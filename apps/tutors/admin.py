# Admin site register yahan kiye hain

"""
Tutors Admin Configuration
"""

from django.contrib import admin
from .models import Subject, Language


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    list_editable = ('is_active', 'icon')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
