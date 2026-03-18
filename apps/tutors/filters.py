"""
Tutor Filters
==============
django-filter integration for advanced tutor directory filtering.
"""

import django_filters
from django.db.models import Q
from apps.accounts.models import TutorProfile
from .models import Subject, Language


class TutorDirectoryFilter(django_filters.FilterSet):
    """Advanced filter for the tutor directory."""

    PRICE_RANGE_CHOICES = (
        ('300-600', '₹300-600/hour'),
        ('600-1000', '₹600-1000/hour'),
        ('1000-1500', '₹1000-1500/hour'),
        ('1500+', '₹1500+/hour'),
    )

    price_range = django_filters.ChoiceFilter(
        method='filter_price_range',
        choices=PRICE_RANGE_CHOICES,
        label='Price Range',
        empty_label='Any Price'
    )

    grade_level = django_filters.ChoiceFilter(
        choices=TutorProfile.GradeLevel.choices,
        label='Grade Level',
        field_name='grade_level',
        empty_label='All Levels'
    )

    # Price range
    min_price = django_filters.NumberFilter(
        field_name='price_per_hour',
        lookup_expr='gte',
        label='Min Price (₹)',
    )
    max_price = django_filters.NumberFilter(
        field_name='price_per_hour',
        lookup_expr='lte',
        label='Max Price (₹)',
    )

    # Subject
    subject = django_filters.ModelMultipleChoiceFilter(
        field_name='subjects',
        queryset=Subject.objects.filter(is_active=True),
        label='Subjects',
    )

    # Language
    language = django_filters.ModelMultipleChoiceFilter(
        field_name='languages',
        queryset=Language.objects.all(),
        label='Languages',
    )

    # Teaching method
    teaching_method = django_filters.ChoiceFilter(
        choices=TutorProfile.TeachingMethod.choices,
        label='Teaching Method',
    )

    # Gender
    gender = django_filters.ChoiceFilter(
        choices=TutorProfile.Gender.choices,
        label='Gender',
    )

    # Experience
    min_experience = django_filters.NumberFilter(
        field_name='experience_years',
        lookup_expr='gte',
        label='Min Experience (years)',
    )

    # Search (name, bio, qualifications)
    search = django_filters.CharFilter(
        method='filter_search',
        label='Search',
    )

    # Sort
    sort_by = django_filters.OrderingFilter(
        fields=(
            ('price_per_hour', 'price'),
            ('experience_years', 'experience'),
            ('created_at', 'newest'),
            ('user__full_name', 'name'),
        ),
        label='Sort By',
    )

    class Meta:
        model = TutorProfile
        fields = []

    def filter_price_range(self, queryset, name, value):
        if value == '300-600':
            return queryset.filter(price_per_hour__gte=300, price_per_hour__lte=600)
        elif value == '600-1000':
            return queryset.filter(price_per_hour__gte=600, price_per_hour__lte=1000)
        elif value == '1000-1500':
            return queryset.filter(price_per_hour__gte=1000, price_per_hour__lte=1500)
        elif value == '1500+':
            return queryset.filter(price_per_hour__gte=1500)
        return queryset

    def filter_search(self, queryset, name, value):
        """Full-text search across name, bio, and qualifications."""
        if value:
            return queryset.filter(
                Q(user__full_name__icontains=value) |
                Q(bio__icontains=value) |
                Q(qualifications__icontains=value) |
                Q(subjects__name__icontains=value)
            ).distinct()
        return queryset
