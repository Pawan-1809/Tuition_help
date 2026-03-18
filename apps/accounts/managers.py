"""
Custom User Manager
====================
Handles user creation with email or phone as primary identifier.
"""

from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Custom manager for User model supporting email/phone authentication."""

    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email and not phone_number:
            raise ValueError('Users must have an email address or phone number.')

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('full_name', 'Admin')

        if not email:
            raise ValueError('Superuser must have an email address.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email=email, password=password, **extra_fields)
