# Admin site register yahan kiye hain

"""
Payments Admin Configuration
"""

from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'razorpay_order_id', 'user', 'amount', 'currency',
        'status', 'created_at'
    )
    list_filter = ('status', 'currency', 'created_at')
    search_fields = (
        'razorpay_order_id', 'razorpay_payment_id',
        'user__email', 'user__full_name'
    )
    readonly_fields = (
        'razorpay_order_id', 'razorpay_payment_id',
        'razorpay_signature', 'created_at', 'updated_at'
    )
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
