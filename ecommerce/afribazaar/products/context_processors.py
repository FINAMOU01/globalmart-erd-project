"""
Context processor for currency selection
Makes the selected currency available to all templates
"""

from payments.models import Currency
from products.currency_utils import get_active_currencies


def currency_context(request):
    """
    Add currency information to template context
    """
    # Get selected currency from session, default to USD
    selected_currency = request.session.get('selected_currency', 'USD')
    
    # Get all active currencies
    currencies = get_active_currencies()
    
    # Get current currency symbol
    try:
        current_currency = Currency.objects.get(currency_code=selected_currency)
        currency_symbol = current_currency.symbol
    except Currency.DoesNotExist:
        currency_symbol = '$'
    
    return {
        'selected_currency': selected_currency,
        'all_currencies': currencies,
        'currency_symbol': currency_symbol,
    }
