"""
Custom template tags for the tutor directory.
"""

from django import template

register = template.Library()


@register.filter
def currency_inr(value):
    """Format a number as Indian Rupees."""
    try:
        value = float(value)
        return f'₹{value:,.0f}'
    except (ValueError, TypeError):
        return value


@register.filter
def star_rating(value, max_stars=5):
    """Convert a numeric rating to star display."""
    try:
        value = float(value)
        full_stars = int(value)
        half_star = 1 if (value - full_stars) >= 0.5 else 0
        empty_stars = max_stars - full_stars - half_star
        return {
            'full': range(full_stars),
            'half': half_star,
            'empty': range(empty_stars),
        }
    except (ValueError, TypeError):
        return {'full': range(0), 'half': 0, 'empty': range(max_stars)}


@register.filter
def truncate_words_smart(value, length=100):
    """Truncate text at word boundary."""
    if len(value) <= length:
        return value
    truncated = value[:length].rsplit(' ', 1)[0]
    return f'{truncated}...'


@register.inclusion_tag('components/social_links.html')
def social_links():
    """Render developer social links."""
    from django.conf import settings
    return {'credits': settings.DEVELOPER_CREDITS}
