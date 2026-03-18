# URLs ki routing yahan par hai

"""
Payments URL Configuration
"""

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('verify/', views.verify_payment_view, name='verify'),
    path('success/', views.payment_success_view, name='success'),
    path('webhook/', views.razorpay_webhook_view, name='webhook'),
]
