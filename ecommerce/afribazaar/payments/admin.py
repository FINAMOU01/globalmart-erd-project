"""
AfriBazaar – Payment & Currency System
Module Owner: NOUDOU

admin.py – Registers all payment models with Django Admin so they can
           be managed through the /admin/ interface.
"""

from django.contrib import admin
from .models import Currency, ExchangeRate


# ─────────────────────────────────────────────────────────────────────────────
# CURRENCY
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display  = ("currency_code", "currency_name", "symbol", "is_active")
    list_filter   = ("is_active",)
    search_fields = ("currency_code", "currency_name")
    ordering      = ("currency_code",)


# ─────────────────────────────────────────────────────────────────────────────
# EXCHANGE RATE
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display  = ("currency", "rate_to_usd", "date_updated")
    list_filter   = ("currency",)
    ordering      = ("-date_updated",)
    date_hierarchy = "date_updated"
