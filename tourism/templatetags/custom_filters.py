from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def range_filter(value):
    """Retourne une range pour les boucles dans les templates"""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)

@register.filter
def multiply(value, arg):
    """Multiplie deux valeurs"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def get_deposit_amount_filter(offer, total_price):
    """Calcule le montant de l'acompte pour une offre donnée"""
    try:
        total_price_decimal = Decimal(str(total_price))
        return offer.get_deposit_amount(total_price_decimal)
    except Exception:
        return Decimal('0.00')
