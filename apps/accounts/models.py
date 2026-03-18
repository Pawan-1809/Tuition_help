# Database models yahan set hain bhai

"""
Accounts Models
================
Custom User model with role-based access, plus TutorProfile and ParentProfile.
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model supporting email/phone authentication with role-based access.
    
    - Tutors: Register, onboard, pay, and publish profiles
    - Parents: Register and browse tutor directory
    - Admins: Access analytics dashboard
    """

    class Role(models.TextChoices):
        TUTOR = 'tutor', 'Tutor'
        PARENT = 'parent', 'Parent/Student'
        ADMIN = 'admin', 'Administrator'

    class AuthProvider(models.TextChoices):
        GOOGLE = 'google', 'Google'
        PHONE = 'phone', 'Phone'
        EMAIL = 'email', 'Email'

    email = models.EmailField('email address', unique=True, blank=True, null=True)
    phone_number = models.CharField('phone number', max_length=15, unique=True, blank=True, null=True)
    full_name = models.CharField('full name', max_length=255)
    role = models.CharField('role', max_length=10, choices=Role.choices, default=Role.PARENT)
    auth_provider = models.CharField(
        'authentication provider', max_length=10,
        choices=AuthProvider.choices, default=AuthProvider.EMAIL
    )
    avatar_url = models.URLField('avatar URL', blank=True, null=True)

    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff status', default=False)
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.full_name or self.email or self.phone_number or 'Unknown User'

    @property
    def is_tutor(self):
        return self.role == self.Role.TUTOR

    @property
    def is_parent(self):
        return self.role == self.Role.PARENT

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN

    @property
    def display_name(self):
        return self.full_name or self.email or self.phone_number


class TutorProfile(models.Model):
    """
    Extended profile for tutors containing teaching details,
    verification status, and multi-step onboarding progress.
    """

    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
        OTHER = 'other', 'Other'

    class TeachingMethod(models.TextChoices):
        ONLINE = 'online', 'Online'
        OFFLINE = 'offline', 'Offline (In-Person)'
        BOTH = 'both', 'Both'

    class GradeLevel(models.TextChoices):
        ALL = 'all', 'All Levels'
        ELEMENTARY = 'elementary', 'Elementary (K-5)'
        MIDDLE = 'middle', 'Middle School (6-8)'
        HIGH = 'high', 'High School (9-12)'
        COLLEGE = 'college', 'College'

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='tutor_profile'
    )

    whatsapp_number = models.CharField(
        'whatsapp number', max_length=15, blank=True, null=True,
        help_text="Format: +919876543210. Used for student connections."
    )
    age = models.PositiveIntegerField('age', null=True, blank=True)
    gender = models.CharField(
        'gender', max_length=10,
        choices=Gender.choices, blank=True
    )

    qualifications = models.TextField('qualifications', blank=True)
    experience_years = models.PositiveIntegerField('years of experience', default=0)
    bio = models.TextField('bio', blank=True, help_text='Short description about the tutor')

    address = models.TextField('address', blank=True)
    latitude = models.FloatField('latitude', null=True, blank=True)
    longitude = models.FloatField('longitude', null=True, blank=True)
    teaching_method = models.CharField(
        'teaching method', max_length=10,
        choices=TeachingMethod.choices, default=TeachingMethod.BOTH
    )
    subjects = models.ManyToManyField(
        'tutors.Subject', blank=True,
        related_name='tutor_profiles',
        verbose_name='subjects'
    )
    languages = models.ManyToManyField(
        'tutors.Language', blank=True,
        related_name='tutor_profiles',
        verbose_name='languages'
    )
    grade_level = models.CharField(
        'grade level', max_length=20,
        choices=GradeLevel.choices, default=GradeLevel.ALL
    )

    price_per_hour = models.DecimalField(
        'price per month (₹)', max_digits=8,
        decimal_places=2, null=True, blank=True
    )

    profile_photo = models.ImageField(
        'profile photo',
        upload_to='profile_photos/%Y/%m/',
        blank=True, null=True
    )

    is_verified = models.BooleanField('verified', default=False)
    is_published = models.BooleanField('published', default=False)
    payment_completed = models.BooleanField('payment completed', default=False)
    onboarding_step = models.PositiveIntegerField('onboarding step', default=1)

    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        db_table = 'tutor_profiles'
        verbose_name = 'Tutor Profile'
        verbose_name_plural = 'Tutor Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"Tutor: {self.user.full_name}"

    @property
    def is_profile_complete(self):
        """Check if all required onboarding fields are filled."""
        required_fields = [
            self.age, self.gender, self.qualifications,
            self.address, self.price_per_hour
        ]
        return all(required_fields) and self.subjects.exists() and self.languages.exists()

    @property
    def can_be_published(self):
        """Profile can only be published if complete and payment is done."""
        return self.is_profile_complete and self.payment_completed

    @property
    def subject_list(self):
        """Comma-separated list of subject names."""
        return ', '.join(self.subjects.values_list('name', flat=True))

    @property
    def language_list(self):
        """Comma-separated list of language names."""
        return ', '.join(self.languages.values_list('name', flat=True))


class ParentProfile(models.Model):
    """Extended profile for parents/students with preferences."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='parent_profile'
    )

    address = models.TextField('address', blank=True)
    latitude = models.FloatField('latitude', null=True, blank=True)
    longitude = models.FloatField('longitude', null=True, blank=True)

    children_count = models.PositiveIntegerField('number of children', default=1)
    preferred_subjects = models.ManyToManyField(
        'tutors.Subject', blank=True,
        related_name='interested_parents',
        verbose_name='preferred subjects'
    )
    preferred_languages = models.ManyToManyField(
        'tutors.Language', blank=True,
        related_name='interested_parents',
        verbose_name='preferred languages'
    )
    preferences = models.JSONField('preferences', default=dict, blank=True)

    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        db_table = 'parent_profiles'
        verbose_name = 'Parent Profile'
        verbose_name_plural = 'Parent Profiles'

    def __str__(self):
        return f"Parent: {self.user.full_name}"
