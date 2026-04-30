"""
AfriBazaar – Payment & Currency System
Module Owner: NOUDOU

forms.py – Django forms for the payments module.

Forms:
    CurrencySelectForm – lightweight form for the currency selector widget
"""

from django import forms
from .models import Currency


class CurrencySelectForm(forms.Form):
    """
    Tiny form used in the currency selector widget (navbar / product page).
    Submits via GET so the selected currency is kept in the session via the view.
    """

    currency_code = forms.ModelChoiceField(
        queryset=Currency.objects.filter(is_active=True),
        to_field_name="currency_code",
        empty_label=None,
        label="",
        widget=forms.Select(
            attrs={"class": "currency-selector", "onchange": "this.form.submit();"}
        ),
    )
