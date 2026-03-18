"""
Razorpay Utility Helpers
=========================
Client initialization and order creation.
"""

import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Razorpay client (lazy initialization)
_razorpay_client = None


def get_razorpay_client():
    """Get or create Razorpay client instance."""
    global _razorpay_client
    if _razorpay_client is None:
        try:
            import razorpay
            _razorpay_client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
            logger.info("Razorpay client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Razorpay client: {e}")
            return None
    return _razorpay_client


def create_razorpay_order(amount_inr, currency='INR', receipt=None, notes=None):
    """
    Create a Razorpay order.
    
    Args:
        amount_inr: Amount in INR (will be converted to paise)
        currency: Currency code (default: INR)
        receipt: Receipt ID for reference
        notes: Dictionary of additional notes
        
    Returns:
        dict: Razorpay order object, or None on failure
    """
    client = get_razorpay_client()
    if client is None:
        logger.error("Razorpay client not available")
        return None

    try:
        order_data = {
            'amount': int(float(amount_inr) * 100),  # Convert to paise
            'currency': currency,
            'receipt': receipt or '',
            'notes': notes or {},
        }
        order = client.order.create(data=order_data)
        logger.info(f"Razorpay order created: {order['id']}")
        return order
    except Exception as e:
        logger.error(f"Failed to create Razorpay order: {e}")
        return None


def verify_razorpay_signature(order_id, payment_id, signature):
    """
    Verify Razorpay payment signature.
    
    Returns:
        bool: True if signature is valid
    """
    client = get_razorpay_client()
    if client is None:
        return False

    try:
        params = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
        }
        client.utility.verify_payment_signature(params)
        logger.info(f"Payment signature verified for order: {order_id}")
        return True
    except Exception as e:
        logger.warning(f"Payment signature verification failed: {e}")
        return False
