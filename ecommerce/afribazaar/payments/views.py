"""
AfriBazaar – Payment & Currency System
Module Owner: NOUDOU

views.py – Views for currency and exchange rate management.

Views:
    currency_rates        – public page listing all active exchange rates
    set_currency          – AJAX/form POST to save chosen currency in session
    api_convert           – JSON endpoint: convert amount between currencies
"""

import json
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.utils import timezone

from .models import Currency, ExchangeRate
from .forms import CurrencySelectForm
from .utils import convert_to_usd, get_active_currencies, get_latest_rate


# ─────────────────────────────────────────────────────────────────────────────
# CURRENCY RATES PAGE
# ─────────────────────────────────────────────────────────────────────────────

def currency_rates(request):
    """
    Public page that lists all active currencies and their latest rates vs USD.

    URL: /payments/currencies/
    Template: payments/currency_rates.html
    """
    currencies = get_active_currencies()

    # For each currency, attach its latest rate
    currency_data = []
    for curr in currencies:
        rate_obj = get_latest_rate(curr.currency_code)
        currency_data.append(
            {
                "currency": curr,
                "rate": rate_obj,
            }
        )

    context = {
        "currency_data": currency_data,
        "last_updated": timezone.now(),
    }
    return render(request, "payments/currency_rates.html", context)


# ─────────────────────────────────────────────────────────────────────────────
# SET CURRENCY (session-based currency selector)
# ─────────────────────────────────────────────────────────────────────────────

@require_POST
def set_currency(request):
    """
    Saves the user's preferred currency in their session.
    Called when the navbar currency selector changes.

    POST body (form or JSON): { "currency_code": "XAF" }
    Redirects back to the referring page (or home).

    URL: /payments/set-currency/
    """
    code = request.POST.get("currency_code", "")
    if Currency.objects.filter(currency_code=code, is_active=True).exists():
        request.session["selected_currency"] = code

    # Redirect back to where the user was
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER", "/")
    return redirect(next_url)


# ─────────────────────────────────────────────────────────────────────────────
# API: CURRENCY CONVERSION  (JSON endpoint for frontend JS)
# ─────────────────────────────────────────────────────────────────────────────

@require_GET
def api_convert(request):
    """
    Converts an amount from one currency to another.

    Query params:
        amount   – the numeric amount to convert
        from     – source currency code (e.g. USD)
        to       – target currency code (e.g. XAF)

    Returns JSON:
        { 
            "success": true, 
            "amount": 1234.56, 
            "rate": 655.957,
            "symbol": "FCFA",
            "formatted": "FCFA 1,234.56" 
        }
    or on error:
        { "success": false, "error": "..." }

    URL: /payments/api/convert/?amount=10&from=USD&to=XAF
    """
    try:
        amount = Decimal(request.GET.get("amount", "0"))
        from_code = request.GET.get("from", "USD").upper()
        to_code = request.GET.get("to", "USD").upper()

        # Convert: from_code → USD → to_code
        usd_amount = convert_to_usd(amount, from_code)

        if to_code == "USD":
            result = usd_amount
            rate = Decimal("1.0")
        else:
            rate_obj = get_latest_rate(to_code)
            if rate_obj is None or rate_obj.rate_to_usd == 0:
                return JsonResponse(
                    {"success": False, "error": f"No exchange rate for {to_code}"}
                )
            result = (usd_amount / rate_obj.rate_to_usd).quantize(Decimal("0.01"))
            rate = rate_obj.rate_to_usd

        try:
            target_currency = Currency.objects.get(currency_code=to_code)
            formatted = f"{target_currency.symbol} {float(result):,.2f}"
            symbol = target_currency.symbol
        except Currency.DoesNotExist:
            formatted = f"{to_code} {float(result):,.2f}"
            symbol = to_code

        return JsonResponse(
            {
                "success": True, 
                "amount": float(result), 
                "rate": float(rate),
                "symbol": symbol,
                "formatted": formatted,
                "currency_code": to_code
            }
        )

    except Exception as exc:
        return JsonResponse({"success": False, "error": str(exc)})
