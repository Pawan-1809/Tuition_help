"""
Dashboard Utility Helpers
==========================
Aggregation and metric calculation functions for the admin dashboard.
"""

from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Sum, Q, F
from django.db.models.functions import TruncMonth, TruncWeek, TruncDate
from django.contrib.auth import get_user_model

from apps.accounts.models import TutorProfile, ParentProfile
from apps.payments.models import Payment

User = get_user_model()


def get_user_stats():
    """Get user registration statistics by role."""
    total_users = User.objects.count()
    stats = User.objects.values('role').annotate(count=Count('id'))

    role_counts = {item['role']: item['count'] for item in stats}

    return {
        'total_users': total_users,
        'total_tutors': role_counts.get('tutor', 0),
        'total_parents': role_counts.get('parent', 0),
        'total_admins': role_counts.get('admin', 0),
    }


def get_tutor_stats():
    """Get tutor-specific statistics."""
    profiles = TutorProfile.objects.all()

    return {
        'total_profiles': profiles.count(),
        'published': profiles.filter(is_published=True).count(),
        'pending_payment': profiles.filter(payment_completed=False).count(),
        'online_tutors': profiles.filter(teaching_method='online').count(),
        'offline_tutors': profiles.filter(teaching_method='offline').count(),
        'both_tutors': profiles.filter(teaching_method='both').count(),
    }


def get_payment_stats():
    """Get payment/revenue statistics."""
    payments = Payment.objects.all()
    captured = payments.filter(status=Payment.Status.CAPTURED)

    return {
        'total_payments': payments.count(),
        'successful_payments': captured.count(),
        'failed_payments': payments.filter(status=Payment.Status.FAILED).count(),
        'total_revenue': captured.aggregate(total=Sum('amount'))['total'] or 0,
        'pending_payments': payments.filter(status=Payment.Status.CREATED).count(),
    }


def get_registration_trend(days=30):
    """Get daily user registration counts for the last N days."""
    start_date = timezone.now() - timedelta(days=days)

    registrations = (
        User.objects
        .filter(date_joined__gte=start_date)
        .annotate(date=TruncDate('date_joined'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    return list(registrations)


def get_revenue_trend(months=6):
    """Get monthly revenue for the last N months."""
    start_date = timezone.now() - timedelta(days=months * 30)

    revenue = (
        Payment.objects
        .filter(status=Payment.Status.CAPTURED, created_at__gte=start_date)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(
            total=Sum('amount'),
            count=Count('id')
        )
        .order_by('month')
    )

    return list(revenue)


def get_subject_distribution():
    """Get distribution of tutors across subjects."""
    from apps.tutors.models import Subject

    distribution = (
        Subject.objects
        .filter(tutor_profiles__is_published=True)
        .annotate(tutor_count=Count('tutor_profiles'))
        .values('name', 'category', 'tutor_count')
        .order_by('-tutor_count')
    )

    return list(distribution)


def get_recent_registrations(limit=10):
    """Get the most recent user registrations."""
    return User.objects.order_by('-date_joined')[:limit]


def get_recent_payments(limit=10):
    """Get the most recent payments."""
    return Payment.objects.select_related('user').order_by('-created_at')[:limit]


def get_all_dashboard_data():
    """Aggregate all dashboard metrics into a single dict."""
    return {
        'users': get_user_stats(),
        'tutors': get_tutor_stats(),
        'payments': get_payment_stats(),
        'registration_trend': get_registration_trend(),
        'revenue_trend': get_revenue_trend(),
        'subject_distribution': get_subject_distribution(),
        'recent_registrations': get_recent_registrations(),
        'recent_payments': get_recent_payments(),
    }
