# Database models yahan set hain bhai

"""
Payment Models
===============
Tracks all Razorpay payment transactions.
"""

from django.db import models
from django.conf import settings


class Payment(models.Model):
    """Records Razorpay payment transactions for tutor registration fees."""

    class Status(models.TextChoices):
        CREATED = 'created', 'Created'
        AUTHORIZED = 'authorized', 'Authorized'
        CAPTURED = 'captured', 'Captured'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    tutor_profile = models.ForeignKey(
        'accounts.TutorProfile',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='payments'
    )

    razorpay_order_id = models.CharField(
        'Razorpay Order ID', max_length=100, unique=True
    )
    razorpay_payment_id = models.CharField(
        'Razorpay Payment ID', max_length=100, blank=True, null=True
    )
    razorpay_signature = models.CharField(
        'Razorpay Signature', max_length=255, blank=True, null=True
    )

    amount = models.DecimalField(
        'amount', max_digits=10, decimal_places=2
    )
    currency = models.CharField(
        'currency', max_length=3, default='INR'
    )
    status = models.CharField(
        'status', max_length=15,
        choices=Status.choices, default=Status.CREATED
    )
    description = models.CharField(
        'description', max_length=255, blank=True,
        default='Tuition Connect - Tutor Registration Fee'
    )

    metadata = models.JSONField('metadata', default=dict, blank=True)

    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"Payment {self.razorpay_order_id} — {self.get_status_display()} — ₹{self.amount}"

    @property
    def is_successful(self):
        return self.status == self.Status.CAPTURED

    @property
    def amount_in_paise(self):
        """Razorpay expects amount in paise (smallest currency unit)."""
        return int(self.amount * 100)
