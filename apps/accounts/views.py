# Views aur business logic idhar hai bhai

"""
Account Views
==============
Authentication views for Google OAuth, Phone/OTP, registration,
and multi-step tutor onboarding.
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from django.db import OperationalError, ProgrammingError
from django.conf import settings

from .forms import (
    PhoneLoginForm, OTPVerifyForm, RoleSelectionForm,
    UserRegistrationForm, LoginForm,
    TutorStep1Form, TutorStep2Form, TutorStep3Form, TutorStep4Form,
    ParentProfileForm,
)
from .models import TutorProfile, ParentProfile
from .utils import send_otp, verify_otp

User = get_user_model()
logger = logging.getLogger(__name__)


def login_view(request):
    """Combined login page with Google OAuth and password options."""
    if request.user.is_authenticated:
        return redirect('accounts:redirect_after_login')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_id = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(request, username=login_id, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.full_name}!')
                return redirect('accounts:redirect_after_login')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
        
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    """Email-based registration with role selection."""
    if request.user.is_authenticated:
        return redirect('accounts:redirect_after_login')

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        role_form = RoleSelectionForm(request.POST)

        try:
            if user_form.is_valid() and role_form.is_valid():
                user = user_form.save(commit=False)
                user.role = role_form.cleaned_data['role']
                user.auth_provider = User.AuthProvider.EMAIL
                user.save()

                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'Welcome to Tuition Connect, {user.full_name}!')
                return redirect('accounts:redirect_after_login')
        except (ProgrammingError, OperationalError):
            logger.exception('Database is not ready for registration.')
            messages.error(
                request,
                'Service is initializing. Please try again in a minute.'
            )
    else:
        user_form = UserRegistrationForm()
        role_form = RoleSelectionForm()

    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'role_form': role_form,
    })


def logout_view(request):
    """Log out and redirect to home."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


def phone_login_view(request):
    """Step 1: Enter phone number to receive OTP."""
    if request.method == 'POST':
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            success = send_otp(phone)
            if success:
                request.session['otp_phone'] = phone
                messages.info(request, 'OTP sent to your phone!')
                return redirect('accounts:verify_otp')
            else:
                messages.error(request, 'Failed to send OTP. Please try again.')
    else:
        form = PhoneLoginForm()

    return render(request, 'accounts/phone_login.html', {'form': form})


def verify_otp_view(request):
    """Step 2: Verify OTP and login/register."""
    phone = request.session.get('otp_phone')
    if not phone:
        messages.warning(request, 'Please enter your phone number first.')
        return redirect('accounts:phone_login')

    if request.method == 'POST':
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if verify_otp(phone, otp):

                user = User.objects.filter(phone_number=phone).first()
                if user:
                    login(request, user, backend='apps.accounts.backends.PhoneOTPBackend')
                    messages.success(request, f'Welcome back, {user.full_name}!')
                    del request.session['otp_phone']
                    return redirect('accounts:redirect_after_login')
                else:

                    request.session['verified_phone'] = phone
                    del request.session['otp_phone']
                    return redirect('accounts:phone_register')
            else:
                messages.error(request, 'Invalid or expired OTP. Please try again.')
    else:
        form = OTPVerifyForm()

    return render(request, 'accounts/verify_otp.html', {
        'form': form,
        'phone': phone,
    })


def phone_register_view(request):
    """Register a new user after phone OTP verification."""
    phone = request.session.get('verified_phone')
    if not phone:
        return redirect('accounts:phone_login')

    if request.method == 'POST':
        role_form = RoleSelectionForm(request.POST)
        if role_form.is_valid():
            full_name = request.POST.get('full_name', '').strip()
            if not full_name:
                messages.error(request, 'Please enter your name.')
            else:
                user = User.objects.create_user(
                    phone_number=phone,
                    full_name=full_name,
                    role=role_form.cleaned_data['role'],
                    auth_provider=User.AuthProvider.PHONE,
                )
                login(request, user, backend='apps.accounts.backends.PhoneOTPBackend')
                del request.session['verified_phone']
                messages.success(request, f'Welcome to Tuition Connect, {user.full_name}!')
                return redirect('accounts:redirect_after_login')
    else:
        role_form = RoleSelectionForm()

    return render(request, 'accounts/phone_register.html', {
        'role_form': role_form,
        'phone': phone,
    })


@login_required
def redirect_after_login(request):
    """Redirect user based on their role after login."""
    user = request.user

    if user.is_admin_user or user.is_superuser:
        return redirect('dashboard:analytics')
    elif user.is_tutor:
        profile = getattr(user, 'tutor_profile', None)
        if profile and profile.is_published:
            return redirect('accounts:profile')
        else:
            return redirect('accounts:onboarding', step=profile.onboarding_step if profile else 1)
    else:
        return redirect('tutors:directory')


ONBOARDING_FORMS = {
    1: ('Personal Information', TutorStep1Form),
    2: ('Qualifications & Experience', TutorStep2Form),
    3: ('Teaching Preferences', TutorStep3Form),
    4: ('Pricing & Review', TutorStep4Form),
}


@login_required
def onboarding_view(request, step=1):
    """Multi-step tutor onboarding."""
    if not request.user.is_tutor:
        messages.warning(request, 'Onboarding is only for tutors.')
        return redirect('tutors:directory')

    profile = get_object_or_404(TutorProfile, user=request.user)

    if step not in ONBOARDING_FORMS:
        return redirect('accounts:onboarding', step=1)

    step_title, FormClass = ONBOARDING_FORMS[step]
    total_steps = len(ONBOARDING_FORMS)

    if request.method == 'POST':
        post_data = request.POST.copy()
        if step == 3:
            from apps.tutors.models import Subject, Language
            posted_subs = post_data.getlist('subjects')
            new_sub_ids = []
            for s in posted_subs:
                if s and not s.isdigit():
                    obj, _ = Subject.objects.get_or_create(name=s.strip(), defaults={'is_active': True})
                    new_sub_ids.append(str(obj.pk))
                elif s:
                    new_sub_ids.append(s)
            post_data.setlist('subjects', new_sub_ids)
            
            posted_langs = post_data.getlist('languages')
            new_lang_ids = []
            for l in posted_langs:
                if l and not l.isdigit():
                    obj, _ = Language.objects.get_or_create(name=l.strip())
                    new_lang_ids.append(str(obj.pk))
                elif l:
                    new_lang_ids.append(l)
            post_data.setlist('languages', new_lang_ids)

        form = FormClass(post_data, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            if step < total_steps:

                profile.onboarding_step = step + 1
                profile.save(update_fields=['onboarding_step'])
                return redirect('accounts:onboarding', step=step + 1)
            else:

                profile.onboarding_step = total_steps + 1
                if settings.DEMO_BYPASS_PAYMENT:
                    profile.is_published = True
                    profile.save(update_fields=['onboarding_step', 'is_published'])
                    messages.success(request, 'Profile complete! Your tutor profile is now live in demo mode.')
                    return redirect('accounts:profile')

                profile.save(update_fields=['onboarding_step'])
                messages.success(request, 'Profile complete! Proceed to payment.')
                return redirect('payments:checkout')
    else:
        form = FormClass(instance=profile)

    return render(request, 'accounts/onboarding.html', {
        'form': form,
        'step': step,
        'step_title': step_title,
        'total_steps': total_steps,
        'profile': profile,
        'progress_percent': int((step / total_steps) * 100),
    })


@login_required
def profile_view(request):
    """User profile page."""
    user = request.user
    context = {'user': user}

    if user.is_tutor:
        profile = get_object_or_404(TutorProfile, user=user)
        context['profile'] = profile
        context['template'] = 'accounts/tutor_profile.html'
    elif user.is_parent:
        profile = get_object_or_404(ParentProfile, user=user)
        if request.method == 'POST':
            form = ParentProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated!')
                return redirect('accounts:profile')
        else:
            form = ParentProfileForm(instance=profile)
        context['profile'] = profile
        context['form'] = form
        context['template'] = 'accounts/parent_profile.html'
    else:
        context['template'] = 'accounts/admin_profile.html'

    return render(request, context.get('template', 'accounts/profile.html'), context)


@login_required
@require_POST
def delete_account_view(request):
    """Delete the requested user account."""
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, 'Your account has been deleted successfully.')
    return redirect('home')


def social_signup_view(request):
    """Handle role selection after Google OAuth signup."""
    if request.method == 'POST':
        role_form = RoleSelectionForm(request.POST)
        if role_form.is_valid():
            user = request.user
            user.role = role_form.cleaned_data['role']
            user.save()

            if user.is_tutor:
                TutorProfile.objects.get_or_create(user=user)
            elif user.is_parent:
                ParentProfile.objects.get_or_create(user=user)
            return redirect('accounts:redirect_after_login')
    else:
        role_form = RoleSelectionForm()

    return render(request, 'accounts/select_role.html', {'role_form': role_form})
