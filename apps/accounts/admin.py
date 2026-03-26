# Admin site register yahan kiye hain

"""
Accounts Admin Configuration
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import TutorProfile, ParentProfile

User = get_user_model()


class TutorProfileInline(admin.StackedInline):
    model = TutorProfile
    can_delete = False
    verbose_name_plural = 'Tutor Profile'
    fk_name = 'user'
    extra = 0
    fieldsets = (
        ('Personal', {
            'fields': ('age', 'gender', 'profile_photo'),
        }),
        ('Qualifications', {
            'fields': ('qualifications', 'experience_years', 'bio'),
        }),
        ('Teaching', {
            'fields': ('address', 'latitude', 'longitude', 'teaching_method', 'subjects', 'languages'),
        }),
        ('Pricing & Status', {
            'fields': ('price_per_hour', 'is_published', 'payment_completed', 'onboarding_step'),
        }),
    )


class ParentProfileInline(admin.StackedInline):
    model = ParentProfile
    can_delete = False
    verbose_name_plural = 'Parent Profile'
    fk_name = 'user'
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'role', 'auth_provider', 'is_active', 'date_joined')
    list_filter = ('role', 'auth_provider', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number', 'avatar_url')}),
        ('Role & Auth', {'fields': ('role', 'auth_provider')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2'),
        }),
    )

    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        if obj.role == User.Role.TUTOR:
            return [TutorProfileInline]
        elif obj.role == User.Role.PARENT:
            return [ParentProfileInline]
        return []


@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'teaching_method', 'price_per_hour', 'is_published', 'payment_completed')
    list_filter = ('is_published', 'payment_completed', 'teaching_method', 'gender')
    search_fields = ('user__full_name', 'user__email', 'address')
    list_editable = ('is_published',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'children_count', 'created_at')
    search_fields = ('user__full_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
