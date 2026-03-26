"""
AfriBazaar – Payment & Currency System
Module Owner: NOUDOU

templatetags/payment_tags.py

Custom template tags and filters for the payments module.

Usage in any template:
    {% load payment_tags %}
    {{ product.base_price|convert_price:request.session.selected_currency }}
    {% currency_selector request %}
"""

from django import template
from django.utils.safestring import mark_safe
from decimal import Decimal

from payments.models import Currency
from payments.utils import get_latest_rate, get_active_currencies

register = template.Library()


# ─────────────────────────────────────────────────────────────────────────────
# FILTER: convert_price
# ─────────────────────────────────────────────────────────────────────────────

@register.filter(name="convert_price")
def convert_price(usd_price, currency_code):
    """
    Template filter that converts a USD price to any currency.

    Usage:
        {{ product.base_price|convert_price:"XAF" }}
        → "FCFA 24,756.00"

        {{ product.base_price|convert_price:session_currency }}
    """
    if not usd_price or not currency_code:
        return usd_price

    usd_price = Decimal(str(usd_price))

    if currency_code == "USD":
        return f"$ {usd_price:,.2f}"

    try:
        currency = Currency.objects.get(currency_code=currency_code, is_active=True)
    except Currency.DoesNotExist:
        return f"$ {usd_price:,.2f}"

    rate_obj = get_latest_rate(currency_code)
    if rate_obj is None or rate_obj.rate_to_usd == 0:
        return f"$ {usd_price:,.2f}"

    converted = (usd_price / rate_obj.rate_to_usd).quantize(Decimal("0.01"))
    return f"{currency.symbol} {converted:,.2f}"


# ─────────────────────────────────────────────────────────────────────────────
# SIMPLE TAG: currency_selector_html
# ─────────────────────────────────────────────────────────────────────────────

@register.simple_tag(takes_context=True)
def currency_selector_html(context):
    """
    Renders an inline <form> with a <select> of all active currencies.
    The currently selected currency (from session) is pre-selected.

    Usage in template:
        {% load payment_tags %}
        {% currency_selector_html %}
    """
    request = context.get("request")
    selected = ""
    if request:
        selected = request.session.get("selected_currency", "USD")

    currencies = get_active_currencies()

    options = ""
    for curr in currencies:
        sel = 'selected="selected"' if curr.currency_code == selected else ""
        options += (
            f'<option value="{curr.currency_code}" {sel}>'
            f'{curr.currency_code} {curr.symbol}</option>'
        )

    html = f"""
    <form method="post" action="/payments/set-currency/" class="currency-selector-form">
        <input type="hidden" name="csrfmiddlewaretoken"
               value="{{{{ csrf_token }}}}">
        <select name="currency_code" class="currency-select"
                onchange="this.form.submit()" title="Select currency">
            {options}
        </select>
    </form>
    """
    return mark_safe(html)
