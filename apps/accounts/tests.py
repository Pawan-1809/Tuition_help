from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .utils import generate_otp, store_otp, verify_otp

# --- PYTHON 3.14 BUG WORKAROUND FOR DJANGO TESTS ---
import copy
from django.template.context import BaseContext, Context, RequestContext

def patched_basecontext_copy(self):
    duplicate = self.__class__.__new__(self.__class__)
    duplicate.dicts = self.dicts[:]
    return duplicate

def patched_requestcontext_copy(self):
    duplicate = patched_basecontext_copy(self)
    if hasattr(self, 'render_context'):
        duplicate.render_context = getattr(self, 'render_context', None)
    duplicate.request = self.request
    return duplicate

BaseContext.__copy__ = patched_basecontext_copy
Context.__copy__ = patched_basecontext_copy
RequestContext.__copy__ = patched_requestcontext_copy
# ---------------------------------------------------

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.register_url = reverse('accounts:register')
        
        # Create a test user
        self.test_user = User.objects.create_user(
            email='testuser@example.com',
            password='securePassword123!',
            full_name='Test User',
            role='parent'
        )

    def test_user_creation(self):
        """Test that user was correctly created in the database"""
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.test_user.email, 'testuser@example.com')
        self.assertEqual(self.test_user.role, 'parent')
        self.assertTrue(self.test_user.check_password('securePassword123!'))

    def test_login_view_success(self):
        """Test logging in with valid credentials"""
        response = self.client.post(self.login_url, {
            'login': 'testuser@example.com',
            'password': 'securePassword123!'
        })
        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_failure(self):
        """Test logging in with incorrect password"""
        response = self.client.post(self.login_url, {
            'login': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200) # Re-renders login form
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, 'Invalid email or password.')

    def test_brute_force_rate_limiting(self):
        """Test django-axes rate locking after 5 failures"""
        for _ in range(5):
            response = self.client.post(self.login_url, {
                'login': 'testuser@example.com',
                'password': 'wrongpassword'
            })
            
        # 6th attempt should return the lockout template (HTTP 429)
        response = self.client.post(self.login_url, {
            'login': 'testuser@example.com',
            'password': 'wrongpassword'
        })
        self.assertContains(response, 'Account Locked Out', status_code=429)
        self.assertEqual(response.status_code, 429)

class OTPUtilityTests(TestCase):
    def setUp(self):
        self.phone = "+1234567890"

    def tearDown(self):
        cache.clear()

    def test_generate_otp(self):
        """Test OTP generation length and randomness"""
        otp = generate_otp(6)
        self.assertTrue(otp.isdigit())
        self.assertEqual(len(otp), 6)

    def test_verify_otp_success(self):
        """Test storing and verifying valid OTP"""
        otp = "123456"
        store_otp(self.phone, otp)
        self.assertTrue(verify_otp(self.phone, "123456"))

    def test_verify_otp_failure(self):
        """Test verifying incorrect OTP"""
        store_otp(self.phone, "123456")
        self.assertFalse(verify_otp(self.phone, "000000"))

    def test_verify_otp_expiration(self):
        """Test OTP validity after cache clears or one-time use"""
        otp = "123456"
        store_otp(self.phone, otp)
        verify_otp(self.phone, otp) # Used once
        # Should now be invalid (deleted from cache)
        self.assertFalse(verify_otp(self.phone, otp))
