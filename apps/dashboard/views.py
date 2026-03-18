# Views aur business logic idhar hai bhai

"""
Dashboard Views
================
Admin analytics dashboard with chart data endpoints.
"""

import json
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .utils import get_all_dashboard_data, get_registration_trend, get_revenue_trend, get_subject_distribution

from .utils import get_all_dashboard_data, get_registration_trend, get_revenue_trend, get_subject_distribution

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

User = get_user_model()


@staff_member_required
def analytics_view(request):
    """Main analytics dashboard for admin/superuser."""
    data = get_all_dashboard_data()
    return render(request, 'dashboard/analytics.html', data)


@staff_member_required
@require_GET
def chart_data_api(request):
    """
    API endpoint returning chart-ready data for the dashboard.
    Used by Chart.js on the frontend.
    """
    chart_type = request.GET.get('type', 'all')

    response = {}

    if chart_type in ('all', 'registrations'):
        trend = get_registration_trend(days=30)
        response['registrations'] = {
            'labels': [item['date'].strftime('%d %b') for item in trend],
            'data': [item['count'] for item in trend],
        }

    if chart_type in ('all', 'revenue'):
        revenue = get_revenue_trend(months=6)
        response['revenue'] = {
            'labels': [item['month'].strftime('%b %Y') for item in revenue],
            'amounts': [float(item['total']) for item in revenue],
            'counts': [item['count'] for item in revenue],
        }

    if chart_type in ('all', 'subjects'):
        distribution = get_subject_distribution()
        response['subjects'] = {
            'labels': [item['name'] for item in distribution],
            'data': [item['tutor_count'] for item in distribution],
            'categories': [item['category'] for item in distribution],
        }

    return JsonResponse(response)


@staff_member_required
def manage_users_view(request, role):
    """View to list and manage users by role (tutor or student/parent)."""
    roles = {'student': 'parent', 'tutor': 'tutor'}
    actual_role = roles.get(role, 'parent')
    
    users = User.objects.filter(role=actual_role).order_by('-date_joined')
    if role == 'tutor':
        users = users.select_related('tutor_profile')
    
    return render(request, 'dashboard/manage_users.html', {
        'users': users,
        'role': role,
        'role_display': 'Tutors' if role == 'tutor' else 'Students / Parents'
    })


@staff_member_required
@require_POST
def delete_user_api(request, user_id):
    """Delete a user account."""
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        messages.error(request, 'Cannot delete an admin user!')
    else:
        user.delete()
        messages.success(request, 'Account deleted successfully.')

    return redirect(request.META.get('HTTP_REFERER', 'dashboard:analytics'))
