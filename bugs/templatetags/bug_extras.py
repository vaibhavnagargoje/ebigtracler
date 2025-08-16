from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """Split a string by delimiter"""
    if value:
        return value.split(delimiter)
    return []

@register.filter
def trim(value):
    """Trim whitespace from string"""
    if value:
        return value.strip()
    return value

@register.filter
def filter_by_status(queryset, status):
    """Filter bugs by status"""
    try:
        return queryset.filter(status=status).count()
    except:
        return 0

@register.filter
def slugify_custom(value):
    """Custom slugify filter for CSS classes"""
    if value:
        return value.lower().replace('_', '-').replace(' ', '-')
    return value
