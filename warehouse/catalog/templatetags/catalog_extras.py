from decimal import Decimal, InvalidOperation

from django import template

from catalog.models import Product

register = template.Library()


@register.filter
def uah(value):
    """Format a price as Ukrainian hryvnia: 1234.5 -> '1,234.50 грн'."""
    try:
        return f'{Decimal(value):,.2f} грн'
    except (InvalidOperation, TypeError, ValueError):
        return value


@register.simple_tag
def product_count():
    """Number of products in the database, shown next to the menu link."""
    return Product.objects.count()