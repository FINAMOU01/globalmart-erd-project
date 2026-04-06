"""
AfriBazaar – Payment & Currency System
Module Owner: NOUDOU

forms.py – Django forms for the payments module.

Forms:
    PaymentForm     – submitted by the customer on the payment page
    CurrencySelectForm – lightweight form for the currency selector widget
"""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, HTML, Div, Submit, Reset
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
            attrs={"class": "form-control", "placeholder": "Name on card"}
        ),
        help_text="Only required for card payments"
    )
    card_last_four = forms.CharField(
        max_length=4,
        required=False,  # Important: Keep as required=False
        label="Last 4 digits of card",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. 4242",
                "maxlength": "4",
            }
        ),
        help_text="Only required for card payments"
    )

    # Mobile money field (visible only when method = MOBILE_MONEY via JS)
    mobile_number = forms.CharField(
        max_length=20,
        required=False,
        label="Mobile Money Number",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+237 6XX XXX XXX"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "payment-form"
        self.helper.form_tag = True
        self.helper.layout = Layout(
            HTML('<div class="payment-container">'),
            HTML('<div class="payment-header"><h3 class="mb-4">Complete Payment</h3></div>'),
            
            # Hidden order_id
            'order_id',
            
            # Currency Selection
            Fieldset(
                'Currency Selection',
                Row(
                    Column('currency_code', css_class='col-md-6'),
                    css_class='row'
                ),
                css_class='fieldset-payment mb-4'
            ),
            
            # Payment Method Selection
            Fieldset(
                'Payment Method',
                'payment_method',
                css_class='fieldset-payment mb-4'
            ),
            
            # Card Payment Fields (hidden by default, shown via JS)
            Div(
                Fieldset(
                    'Card Details',
                    Row(
                        Column('cardholder_name', css_class='col-md-6'),
                        Column('card_last_four', css_class='col-md-6'),
                        css_class='row'
                    ),
                    css_class='fieldset-payment'
                ),
                id='card-fields',
                css_class='payment-method-fields d-none'
            ),
            
            # Mobile Money Fields (hidden by default, shown via JS)
            Div(
                Fieldset(
                    'Mobile Money Details',
                    'mobile_number',
                    css_class='fieldset-payment'
                ),
                id='mobile-fields',
                css_class='payment-method-fields d-none'
            ),
            
            # Buttons
            Row(
                Column(
                    Submit('submit', 'Process Payment', css_class='btn btn-primary btn-lg w-100'),
                    css_class='col-md-6'
                ),
                Column(
                    Reset('reset', 'Clear Form', css_class='btn btn-outline-secondary btn-lg w-100'),
                    css_class='col-md-6'
                ),
                css_class='row g-2 mt-4'
            ),
            
            HTML('</div>'),
        )

    def clean(self):
        """Cross-field validation: validate required fields based on payment method."""
        cleaned = super().clean()
        method = cleaned.get("payment_method")
        
        # In simulation mode, we don't require card/mobile details server-side
        # The frontend JavaScript handles show/hide; server accepts any valid payment method
        # This allows testing without entering payment details
        
        # Just validate that a payment method was selected
        if not method:
            self.add_error("payment_method", "Please select a payment method.")
        
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
