"""
AfriBazaar – Payment & Currency System
Module Owner: NOUDOU

utils.py – Helper functions used across the payments module.

Functions:
    get_latest_rate(currency_code) → Decimal | None
    convert_to_usd(amount, currency_code) → Decimal
    convert_from_usd(amount_usd, currency_code) → Decimal
    get_active_currencies() → QuerySet[Currency]
    format_amount(amount, currency) → str
"""

from decimal import Decimal, ROUND_HALF_UP
from .models import Currency, ExchangeRate


def get_latest_rate(currency_code):
    """
    Return the most recent ExchangeRate object for the given currency code.
    Returns None if no rate exists.

    Usage:
        rate_obj = get_latest_rate("XAF")
        if rate_obj:
            print(rate_obj.rate_to_usd)
    """
    try:
        return (
            ExchangeRate.objects
            .filter(currency__currency_code=currency_code)
            .order_by("-date_updated")
            .first()
        )
    except Exception:
        return None


def convert_to_usd(amount, currency_code):
    """
    Convert an amount from the given currency to USD.

    If no exchange rate exists for the currency, the original amount is
    returned unchanged (graceful degradation).

    Args:
        amount (Decimal | float | int): Amount in the source currency
        currency_code (str): ISO code of the source currency, e.g. "XAF"

    Returns:
        Decimal: Equivalent amount in USD, rounded to 2 decimal places
    """
    amount = Decimal(str(amount))

    if currency_code == "USD":
        return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    rate_obj = get_latest_rate(currency_code)
    if rate_obj is None:
        # No rate found – return as-is (will be flagged in the UI)
        return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    usd_value = amount * rate_obj.rate_to_usd
    return usd_value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def convert_from_usd(amount_usd, currency_code):
    """
    Convert an amount from USD to the given currency.

    Args:
        amount_usd (Decimal | float | int): Amount in USD
        currency_code (str): ISO code of the target currency

    Returns:
        Decimal: Equivalent amount in the target currency, rounded to 2 dp
    """
    amount_usd = Decimal(str(amount_usd))

    if currency_code == "USD":
        return amount_usd.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    rate_obj = get_latest_rate(currency_code)
    if rate_obj is None or rate_obj.rate_to_usd == 0:
        return amount_usd.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    local_value = amount_usd / rate_obj.rate_to_usd
    return local_value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def get_active_currencies():
    """Return all active Currency objects ordered by currency code."""
    return Currency.objects.filter(is_active=True).order_by("currency_code")


def format_amount(amount, currency):
    """
    Return a formatted string like "₦ 5,200.00" or "$ 10.50".

    Args:
        amount (Decimal | float): The amount
        currency (Currency): A Currency model instance

    Returns:
        str
    """
    amount = Decimal(str(amount))
    formatted = f"{amount:,.2f}"
    return f"{currency.symbol} {formatted}"
