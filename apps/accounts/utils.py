"""
Account Utilities
==================
OTP generation, verification, and SMS sending helpers.
"""

import random
import logging
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)


def generate_otp(length=6):
    """Generate a random numeric OTP."""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def store_otp(phone_number, otp):
    """Store OTP in cache with expiry."""
    cache_key = f'otp_{phone_number}'
    expiry = getattr(settings, 'OTP_EXPIRY_SECONDS', 300)
    cache.set(cache_key, otp, timeout=expiry)
    logger.info(f"OTP stored for {phone_number} (expires in {expiry}s)")


def verify_otp(phone_number, otp):
    """Verify OTP against cached value."""
    cache_key = f'otp_{phone_number}'
    cached_otp = cache.get(cache_key)

    if cached_otp is None:
        logger.warning(f"OTP expired or not found for {phone_number}")
        return False

    if str(cached_otp) == str(otp):
        cache.delete(cache_key)  # One-time use
        logger.info(f"OTP verified for {phone_number}")
        return True

    logger.warning(f"Invalid OTP attempt for {phone_number}")
    return False


def send_otp_sms(phone_number, otp):
    """
    Send OTP via SMS provider.
    
    TODO: Integrate with Twilio or another SMS provider.
    For now, logs the OTP to console (development mode).
    """
    if settings.DEBUG:
        logger.info(f"[DEV] OTP for {phone_number}: {otp}")
        print(f"\n{'='*40}")
        print(f"  📱 OTP for {phone_number}: {otp}")
        print(f"{'='*40}\n")
        return True

    # Production: Integrate with SMS provider
    # from twilio.rest import Client
    # client = Client(settings.SMS_PROVIDER_SID, settings.SMS_PROVIDER_AUTH_TOKEN)
    # message = client.messages.create(
    #     body=f'Your Tuition Connect OTP is: {otp}',
    #     from_=settings.SMS_PROVIDER_PHONE,
    #     to=phone_number
    # )
    # return message.sid is not None

    logger.error("SMS provider not configured for production")
    return False


def send_otp(phone_number):
    """Generate, store, and send OTP to a phone number."""
    otp = generate_otp()
    store_otp(phone_number, otp)
    success = send_otp_sms(phone_number, otp)
    return success
