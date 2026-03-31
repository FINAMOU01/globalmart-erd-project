"""
Currency conversion utilities for AfriBazaar
Handles converting prices between different currencies
"""

from decimal import Decimal
from django import template
from payments.models import Currency, ExchangeRate

register = template.Library()


def get_active_currencies():
    """Get all active currencies available for selection"""
    return Currency.objects.filter(is_active=True).order_by('currency_code')


def get_currency_symbol(currency_code):
    """Get the symbol for a currency code"""
    try:
        currency = Currency.objects.get(currency_code=currency_code)
        return currency.symbol
    except Currency.DoesNotExist:
        return currency_code


def get_latest_exchange_rate(currency_code):
    """Get the latest exchange rate for a currency"""
    try:
        rate = ExchangeRate.objects.filter(
            currency_code=currency_code
        ).latest('date_updated')
        return rate.rate_to_usd
    except ExchangeRate.DoesNotExist:
        # Default to 1.0 if rate not found
        return Decimal('1.0')


def convert_price(amount, from_currency, to_currency):
    """
    Convert price from one currency to another
    
    Args:
        amount: The price to convert (Decimal or float)
        from_currency: Source currency code (e.g., 'USD')
        to_currency: Target currency code (e.g., 'EUR')
    
    Returns:
        Converted amount as Decimal, rounded to 2 places
    """
    if from_currency == to_currency:
        return Decimal(str(amount))
    
    try:
        from_rate = get_latest_exchange_rate(from_currency)
        to_rate = get_latest_exchange_rate(to_currency)
        
        # Convert: amount * (from_rate / to_rate)
        converted = Decimal(str(amount)) * (Decimal(str(from_rate)) / Decimal(str(to_rate)))
        return round(converted, 2)
    except Exception as e:
        print(f"Currency conversion error: {e}")
        return Decimal(str(amount))


def format_price(amount, currency_code):
    """
    Format price with currency symbol
    
    Args:
        amount: The price value
        currency_code: Currency code (e.g., 'USD')
    
    Returns:
        Formatted string like "$ 29.99"
    """
    symbol = get_currency_symbol(currency_code)
    return f"{symbol} {amount:,.2f}"


# Django template filter for converting prices
@register.filter
def convert_to_currency(product, target_currency):
    """
    Template filter to convert product price to target currency
    Usage: {{ product|convert_to_currency:selected_currency }}
    """
    if hasattr(product, 'get_price_in_currency'):
        converted = product.get_price_in_currency(target_currency)
        return converted
    return product.price
