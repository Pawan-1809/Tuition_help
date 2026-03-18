"""
Phone OTP Authentication Backend
==================================
Allows users to authenticate via phone number + OTP.
"""

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class PhoneOTPBackend(BaseBackend):
    """
    Custom authentication backend for phone number + OTP login.
    OTP verification is handled in the view before calling authenticate().
    """

    def authenticate(self, request, phone_number=None, **kwargs):
        """Authenticate user by phone number (OTP already verified in view)."""
        if phone_number is None:
            return None
        try:
            user = User.objects.get(phone_number=phone_number, is_active=True)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """Retrieve user by primary key."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class EmailOrPhoneBackend(BaseBackend):
    """
    Custom authentication backend for email or phone + password login.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
            
        try:
            # Check if input is phone number or email
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(phone_number=username)
                
        except User.DoesNotExist:
            return None
            
        if user.check_password(password) and user.is_active:
            return user
            
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
