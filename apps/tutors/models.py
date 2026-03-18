# Database models yahan set hain bhai

"""
Tutors Models
==============
Lookup tables for subjects and languages.
"""

from django.db import models


class Subject(models.Model):
    """Subjects that tutors can teach."""

    class Category(models.TextChoices):
        ACADEMIC = 'academic', 'Academic'
        COMPETITIVE = 'competitive', 'Competitive Exams'
        SKILL = 'skill', 'Skill-based'
        LANGUAGE = 'language', 'Language Learning'

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=15,
        choices=Category.choices,
        default=Category.ACADEMIC
    )
    icon = models.CharField(
        max_length=50, blank=True,
        help_text='Lucide icon name (e.g., "calculator", "book-open")'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'subjects'
        ordering = ['category', 'name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.name


class Language(models.Model):
    """Vocal/teaching languages available."""

    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(
        max_length=5, unique=True,
        help_text='ISO 639-1 language code (e.g., "en", "hi")'
    )

    class Meta:
        db_table = 'languages'
        ordering = ['name']
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Ratings and reviews for tutors."""
    tutor = models.ForeignKey('accounts.TutorProfile', on_delete=models.CASCADE, related_name='reviews')
    parent = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='given_reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        ordering = ['-created_at']
        unique_together = ('tutor', 'parent')

    def __str__(self):
        return f"{self.rating} stars for {self.tutor.user.full_name} by {self.parent.full_name}"
