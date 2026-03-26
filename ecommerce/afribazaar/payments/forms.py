"""
AfriBazaar – Payment & Currency System
Module Owner: NOUDOU

forms.py – Django forms for the payments module.

Forms:
    PaymentForm     – submitted by the customer on the payment page
    CurrencySelectForm – lightweight form for the currency selector widget
"""

from django import forms
from .models import Payment, Currency


class PaymentForm(forms.Form):
    """
    Form presented to the customer on the payment page.

    Fields:
        order_id         – the order being paid (hidden, filled by the view)
        currency_code    – currency the customer wants to pay in
        payment_method   – how they want to pay
        cardholder_name  – shown only for card payments (frontend handles show/hide)
        card_number      – last 4 digits only for demo (never store real card numbers!)
    """

    order_id = forms.IntegerField(widget=forms.HiddenInput())

    currency_code = forms.ModelChoiceField(
        queryset=Currency.objects.filter(is_active=True),
        to_field_name="currency_code",
        empty_label="Select currency",
        label="Pay in",
        widget=forms.Select(attrs={"class": "form-select", "id": "id_currency_code"}),
    )

    payment_method = forms.ChoiceField(
        choices=Payment.PAYMENT_METHOD_CHOICES,
        label="Payment Method",
        widget=forms.RadioSelect(attrs={"class": "payment-method-radio"}),
    )

    # Card-specific fields (visible only when method = CARD via JS)
    cardholder_name = forms.CharField(
        max_length=100,
        required=False,
        label="Cardholder Name",
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "Name on card"}
        ),
    )
    card_last_four = forms.CharField(
        max_length=4,
        min_length=4,
        required=False,
        label="Last 4 digits of card",
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "e.g. 4242",
                "maxlength": "4",
            }
        ),
    )

    # Mobile money field (visible only when method = MOBILE_MONEY via JS)
    mobile_number = forms.CharField(
        max_length=20,
        required=False,
        label="Mobile Money Number",
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "+237 6XX XXX XXX"}
        ),
    )

    def clean(self):
        """Cross-field validation: card fields required when method is CARD."""
        cleaned = super().clean()
        method = cleaned.get("payment_method")
        if method == Payment.METHOD_CARD:
            if not cleaned.get("cardholder_name"):
                self.add_error("cardholder_name", "Please enter the cardholder name.")
            if not cleaned.get("card_last_four"):
                self.add_error("card_last_four", "Please enter the last 4 digits.")
        if method == Payment.METHOD_MOBILE_MONEY:
            if not cleaned.get("mobile_number"):
                self.add_error("mobile_number", "Please enter your mobile money number.")
        return cleaned


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
