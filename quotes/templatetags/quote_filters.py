from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def approx_time(value):
    diff = timezone.now() - value
    seconds = diff.total_seconds()

    if seconds < 300:
        return "now"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minutes ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds // 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 2592000:
        weeks = int(seconds // 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    else:
        months = int(seconds // 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"
