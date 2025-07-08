from django import template

register = template.Library()

@register.filter
def range(value):
    """Retourne une range pour les boucles dans les templates"""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)
