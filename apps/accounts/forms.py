"""
Account Forms
==============
Registration, login, and multi-step onboarding forms.
"""

from django import forms
from django.contrib.auth import get_user_model
from .models import TutorProfile, ParentProfile

User = get_user_model()


# ── Neumorphic form widget attrs ──────────────────────
NEUMORPHIC_INPUT = {
    'class': 'neu-input',
    'autocomplete': 'off',
}

NEUMORPHIC_SELECT = {
    'class': 'neu-select',
}

NEUMORPHIC_TEXTAREA = {
    'class': 'neu-textarea',
    'rows': 4,
}

NEUMORPHIC_SELECT_MULTIPLE = {
    'class': 'neu-select-multiple',
}


class PhoneLoginForm(forms.Form):
    """Step 1: Enter phone number to receive OTP."""
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            **NEUMORPHIC_INPUT,
            'placeholder': '+91 98765 43210',
            'type': 'tel',
            'id': 'phone-input',
        }),
        help_text='Enter your phone number with country code',
    )


class LoginForm(forms.Form):
    """Login with Email and Password."""
    login = forms.CharField(
        label='Email Address',
        widget=forms.TextInput(attrs={
            **NEUMORPHIC_INPUT,
            'placeholder': 'your@email.com',
        }),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            **NEUMORPHIC_INPUT,
            'placeholder': 'Your password',
        }),
    )


class OTPVerifyForm(forms.Form):
    """Step 2: Verify OTP sent to phone."""
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            **NEUMORPHIC_INPUT,
            'placeholder': '● ● ● ● ● ●',
            'id': 'otp-input',
            'inputmode': 'numeric',
            'pattern': '[0-9]{6}',
            'maxlength': '6',
        }),
    )


class RoleSelectionForm(forms.Form):
    """Select role after phone/Google signup."""
    role = forms.ChoiceField(
        choices=[
            ('tutor', 'I am a Tutor'),
            ('parent', 'I am a Parent/Student'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'neu-radio'}),
    )


class UserRegistrationForm(forms.ModelForm):
    """Email-based registration form."""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            **NEUMORPHIC_INPUT,
            'placeholder': 'Create a strong password',
        }),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            **NEUMORPHIC_INPUT,
            'placeholder': 'Confirm your password',
        }),
    )

    class Meta:
        model = User
        fields = ['full_name', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={
                **NEUMORPHIC_INPUT,
                'placeholder': 'Your full name',
            }),
            'email': forms.EmailInput(attrs={
                **NEUMORPHIC_INPUT,
                'placeholder': 'your@email.com',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1, p2 = cleaned_data.get('password1'), cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# ── Tutor Onboarding Steps ────────────────────────────

class TutorStep1Form(forms.ModelForm):
    """Step 1: Personal Information."""

    class Meta:
        model = TutorProfile
        fields = ['whatsapp_number', 'age', 'gender', 'profile_photo']
        widgets = {
            'whatsapp_number': forms.TextInput(attrs={
                **NEUMORPHIC_INPUT,
                'placeholder': '+91 98765 43210 (WhatsApp)',
                'type': 'tel',
            }),
            'age': forms.NumberInput(attrs={
                **NEUMORPHIC_INPUT,
                'placeholder': 'Your age',
                'min': '18',
                'max': '80',
            }),
            'gender': forms.Select(attrs=NEUMORPHIC_SELECT),
            'profile_photo': forms.ClearableFileInput(attrs={
                'class': 'neu-file-input',
                'accept': 'image/*',
            }),
        }


class TutorStep2Form(forms.ModelForm):
    """Step 2: Qualifications & Experience."""

    class Meta:
        model = TutorProfile
        fields = ['qualifications', 'experience_years', 'bio']
        widgets = {
            'qualifications': forms.Textarea(attrs={
                **NEUMORPHIC_TEXTAREA,
                'placeholder': 'e.g., B.Ed, M.Sc Mathematics, IIT Graduate...',
            }),
            'experience_years': forms.NumberInput(attrs={
                **NEUMORPHIC_INPUT,
                'placeholder': 'Years of teaching experience',
                'min': '0',
            }),
            'bio': forms.Textarea(attrs={
                **NEUMORPHIC_TEXTAREA,
                'placeholder': 'Tell parents about yourself and your teaching style...',
            }),
        }


class TutorStep3Form(forms.ModelForm):
    """Step 3: Teaching Preferences & Location."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['languages'].label = "Suitable Language"
        self.fields['subjects'].label = "Subjects (Select or Type new)"
        self.fields['grade_level'].label = "Which grade students will you teach?"

    class Meta:
        model = TutorProfile
        fields = ['address', 'teaching_method', 'grade_level', 'subjects', 'languages']
        widgets = {
            'address': forms.Textarea(attrs={
                **NEUMORPHIC_TEXTAREA,
                'placeholder': 'Your complete address for location-based matching...',
                'rows': 3,
            }),
            'teaching_method': forms.Select(attrs=NEUMORPHIC_SELECT),
            'grade_level': forms.Select(attrs=NEUMORPHIC_SELECT),
            'subjects': forms.SelectMultiple(attrs=NEUMORPHIC_SELECT_MULTIPLE),
            'languages': forms.SelectMultiple(attrs=NEUMORPHIC_SELECT_MULTIPLE),
        }


class TutorStep4Form(forms.ModelForm):
    """Step 4: Pricing."""

    class Meta:
        model = TutorProfile
        fields = ['price_per_hour']
        widgets = {
            'price_per_hour': forms.NumberInput(attrs={
                **NEUMORPHIC_INPUT,
                'placeholder': 'Price per month in ₹',
                'min': '100',
                'step': '50',
            }),
        }


class ParentProfileForm(forms.ModelForm):
    """Parent/Student profile editing form."""

    class Meta:
        model = ParentProfile
        fields = ['address', 'children_count', 'preferred_subjects', 'preferred_languages']
        widgets = {
            'address': forms.Textarea(attrs={
                **NEUMORPHIC_TEXTAREA,
                'placeholder': 'Your location for nearby tutor search...',
                'rows': 3,
            }),
            'children_count': forms.NumberInput(attrs={
                **NEUMORPHIC_INPUT,
                'placeholder': 'Number of children',
                'min': '1',
            }),
            'preferred_subjects': forms.SelectMultiple(attrs=NEUMORPHIC_SELECT_MULTIPLE),
            'preferred_languages': forms.SelectMultiple(attrs=NEUMORPHIC_SELECT_MULTIPLE),
        }
