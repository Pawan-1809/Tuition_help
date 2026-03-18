# URLs ki routing yahan par hai

"""
Account URL Configuration
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('phone/login/', views.phone_login_view, name='phone_login'),
    path('phone/verify/', views.verify_otp_view, name='verify_otp'),
    path('phone/register/', views.phone_register_view, name='phone_register'),

    path('redirect/', views.redirect_after_login, name='redirect_after_login'),

    path('social/signup/', views.social_signup_view, name='social_signup'),

    path('onboarding/<int:step>/', views.onboarding_view, name='onboarding'),

    path('profile/', views.profile_view, name='profile'),

    path('delete/', views.delete_account_view, name='delete_account'),
]
