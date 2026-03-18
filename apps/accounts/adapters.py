"""
Social Account Adapter
=======================
Customizes the allauth social login flow for Tuition Connect.
"""

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()


class TuitionSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom social account adapter to handle Google OAuth signups."""

    def pre_social_login(self, request, sociallogin):
        """
        If a user with this email already exists, connect the social account
        to the existing user instead of creating a new one.
        """
        if sociallogin.is_existing:
            return

        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass

    def save_user(self, request, sociallogin, form=None):
        """Customize user creation from social login."""
        user = super().save_user(request, sociallogin, form)

        # Set auth provider
        user.auth_provider = User.AuthProvider.GOOGLE

        # Extract name from social data
        extra_data = sociallogin.account.extra_data
        if not user.full_name:
            user.full_name = extra_data.get('name', '')

        # Set avatar URL
        user.avatar_url = extra_data.get('picture', '')

        user.save()
        return user

    def get_login_redirect_url(self, request):
        """Redirect to role selection if role not set."""
        user = request.user
        if user.role == User.Role.PARENT and not hasattr(user, 'parent_profile'):
            return '/accounts/social/signup/'
        return '/accounts/redirect/'
