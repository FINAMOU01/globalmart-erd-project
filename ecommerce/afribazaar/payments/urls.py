"""
AfriBazaar – Payment & Currency System
Module Owner: NOUDOU

urls.py – URL routes for the payments app.
These are included in the project root urls.py under the prefix /payments/

Routes:
    /payments/pay/                  → payment_page
    /payments/confirmation/         → payment_confirmation
    /payments/failed/               → payment_failed
    /payments/currencies/           → currency_rates
    /payments/set-currency/         → set_currency
    /payments/api/convert/          → api_convert
"""

from django.urls import path
from . import views

# app_name allows reverse() to use namespaced URLs: reverse('payments:payment_page')
app_name = "payments"

urlpatterns = [
    path("pay/",          views.payment_page,         name="payment_page"),
    path("confirmation/", views.payment_confirmation, name="payment_confirmation"),
    path("failed/",       views.payment_failed,        name="payment_failed"),
    path("currencies/",   views.currency_rates,        name="currency_rates"),
    path("set-currency/", views.set_currency,           name="set_currency"),
    path("api/convert/",  views.api_convert,            name="api_convert"),
]
