"""
Tuition Connect — Root URL Configuration
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import render


def health_check(request):
    """Simple health check endpoint for Docker."""
    return JsonResponse({'status': 'healthy', 'app': 'Tuition Connect'})


def home_view(request):
    """Landing page."""
    from apps.accounts.models import TutorProfile
    from django.contrib.auth import get_user_model
    User = get_user_model()

    context = {
        'total_tutors': TutorProfile.objects.filter(is_published=True).count(),
        'total_users': User.objects.count(),
    }
    return render(request, 'home.html', context)


urlpatterns = [
    # Home
    path('', home_view, name='home'),

    # Health check
    path('health/', health_check, name='health_check'),

    # Django Admin fallback
    path('django-admin/', admin.site.urls),

    # Authentication (allauth + custom)
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),

    # Tutors directory
    path('tutors/', include('apps.tutors.urls', namespace='tutors')),

    # Payments
    path('payments/', include('apps.payments.urls', namespace='payments')),

    # Dashboard moved to /admin/
    path('admin/', include('apps.dashboard.urls', namespace='dashboard')),

    # Chat
    path('chat/', include('apps.chat.urls', namespace='chat')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin site customization
admin.site.site_header = 'Tuition Connect Administration'
admin.site.site_title = 'Tuition Connect Admin'
admin.site.index_title = 'Dashboard'
