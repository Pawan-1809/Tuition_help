"""
Account Signals
================
Auto-create role-specific profiles when a new user is created.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, TutorProfile, ParentProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create the corresponding profile when a new user registers."""
    if created:
        if instance.role == User.Role.TUTOR:
            TutorProfile.objects.get_or_create(user=instance)
        elif instance.role == User.Role.PARENT:
            ParentProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the corresponding profile when the user is saved."""
    if instance.role == User.Role.TUTOR and hasattr(instance, 'tutor_profile'):
        instance.tutor_profile.save()
    elif instance.role == User.Role.PARENT and hasattr(instance, 'parent_profile'):
        instance.parent_profile.save()
