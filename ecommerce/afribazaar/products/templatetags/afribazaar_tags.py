"""
Custom template tags and filters for AfriBazaar
"""

from django import template

register = template.Library()


@register.filter
def convert_to_currency(product, target_currency):
    """
    Template filter to convert product price to target currency
    Usage: {{ product|convert_to_currency:selected_currency }}
    """
    if hasattr(product, 'get_price_in_currency'):
        try:
            converted = product.get_price_in_currency(target_currency)
            return converted
        except Exception as e:
            print(f"Conversion error: {e}")
            return product.price
    return product.price


@register.filter
def currency_format(amount, currency_code):
    """
    Format amount with currency symbol
    Usage: {{ price|currency_format:currency_code }}
    """
    try:
        from products.currency_utils import get_currency_symbol
        symbol = get_currency_symbol(currency_code)
        return f"{symbol} {float(amount):,.2f}"
    except Exception as e:
        print(f"Format error: {e}")
        return f"{amount:,.2f}"


@register.filter
def get_currency_symbol(currency_code):
    """
    Get the symbol for a currency code
    Usage: {{ 'USD'|get_currency_symbol }}
    """
    from payments.models import Currency
    try:
        currency = Currency.objects.get(currency_code=currency_code)
        return currency.symbol
    except:
        return currency_code
