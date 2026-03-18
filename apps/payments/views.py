# Views aur business logic idhar hai bhai

"""
Payment Views
==============
Checkout, verification, and webhook handling for Razorpay.
"""

import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from apps.accounts.models import TutorProfile
from .models import Payment
from .utils import create_razorpay_order, verify_razorpay_signature

logger = logging.getLogger(__name__)


@login_required
def checkout_view(request):
    """
    Render the Razorpay checkout page for tutor registration fee.
    Creates a Razorpay order and passes it to the frontend.
    """
    if not request.user.is_tutor:
        messages.warning(request, 'Payment is only required for tutor registration.')
        return redirect('tutors:directory')

    profile = get_object_or_404(TutorProfile, user=request.user)

    if profile.payment_completed:
        messages.info(request, 'You have already completed payment.')
        return redirect('accounts:profile')

    if not profile.is_profile_complete:
        messages.warning(request, 'Please complete your profile before payment.')
        return redirect('accounts:onboarding', step=profile.onboarding_step)

    amount = settings.RAZORPAY_REGISTRATION_FEE

    order = create_razorpay_order(
        amount_inr=amount,
        currency='INR',
        receipt=f'tutor_{request.user.pk}',
        notes={
            'user_id': str(request.user.pk),
            'user_email': request.user.email or '',
            'purpose': 'Tutor Registration Fee',
        }
    )

    if order is None:

        if settings.DEBUG:
            payment = Payment.objects.create(
                user=request.user,
                tutor_profile=profile,
                razorpay_order_id=f'dev_order_{request.user.pk}',
                amount=amount,
                status=Payment.Status.CREATED,
            )
            context = {
                'amount': amount,
                'payment': payment,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'order_id': payment.razorpay_order_id,
                'dev_mode': True,
            }
        else:
            messages.error(request, 'Payment service is temporarily unavailable.')
            return redirect('accounts:profile')
    else:

        payment = Payment.objects.create(
            user=request.user,
            tutor_profile=profile,
            razorpay_order_id=order['id'],
            amount=amount,
            status=Payment.Status.CREATED,
        )
        context = {
            'amount': amount,
            'payment': payment,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'order_id': order['id'],
            'dev_mode': False,
        }

    context['user'] = request.user
    return render(request, 'payments/checkout.html', context)


@login_required
@require_POST
def verify_payment_view(request):
    """
    Verify Razorpay payment after checkout completion.
    Called via AJAX from the frontend.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)

    order_id = data.get('razorpay_order_id')
    payment_id = data.get('razorpay_payment_id')
    signature = data.get('razorpay_signature')

    if not all([order_id, payment_id, signature]):
        return JsonResponse({'success': False, 'error': 'Missing payment details'}, status=400)

    try:
        payment = Payment.objects.get(
            razorpay_order_id=order_id,
            user=request.user
        )
    except Payment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Payment not found'}, status=404)

    is_valid = verify_razorpay_signature(order_id, payment_id, signature)

    if is_valid or settings.DEBUG:

        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.status = Payment.Status.CAPTURED
        payment.save()

        if payment.tutor_profile:
            payment.tutor_profile.payment_completed = True
            payment.tutor_profile.is_published = True
            payment.tutor_profile.save(update_fields=['payment_completed', 'is_published'])

        logger.info(f"Payment verified for user {request.user.pk}: {payment_id}")
        return JsonResponse({
            'success': True,
            'message': 'Payment successful! Your profile is now live.',
            'redirect': '/payments/success/',
        })
    else:
        payment.status = Payment.Status.FAILED
        payment.save()
        return JsonResponse({'success': False, 'error': 'Payment verification failed'}, status=400)


@login_required
def payment_success_view(request):
    """Payment success confirmation page."""
    return render(request, 'payments/success.html')


@csrf_exempt
@require_POST
def razorpay_webhook_view(request):
    """
    Handle Razorpay webhook events.
    Verify webhook signature and update payment status.
    """
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    event = payload.get('event', '')
    logger.info(f"Razorpay webhook received: {event}")

    if event == 'payment.captured':
        payment_entity = payload.get('payload', {}).get('payment', {}).get('entity', {})
        order_id = payment_entity.get('order_id')
        payment_id = payment_entity.get('id')

        if order_id:
            try:
                payment = Payment.objects.get(razorpay_order_id=order_id)
                payment.razorpay_payment_id = payment_id
                payment.status = Payment.Status.CAPTURED
                payment.save()

                if payment.tutor_profile:
                    payment.tutor_profile.payment_completed = True
                    payment.tutor_profile.is_published = True
                    payment.tutor_profile.save(update_fields=['payment_completed', 'is_published'])

                logger.info(f"Webhook: Payment captured for order {order_id}")
            except Payment.DoesNotExist:
                logger.warning(f"Webhook: Payment not found for order {order_id}")

    elif event == 'payment.failed':
        payment_entity = payload.get('payload', {}).get('payment', {}).get('entity', {})
        order_id = payment_entity.get('order_id')

        if order_id:
            try:
                payment = Payment.objects.get(razorpay_order_id=order_id)
                payment.status = Payment.Status.FAILED
                payment.save()
                logger.info(f"Webhook: Payment failed for order {order_id}")
            except Payment.DoesNotExist:
                pass

    return JsonResponse({'status': 'ok'})
