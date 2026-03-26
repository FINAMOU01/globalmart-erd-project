"""
AfriBazaar – Payment & Currency System
Module Owner: NOUDOU

admin.py – Registers all payment models with Django Admin so they can
           be managed through the /admin/ interface.
"""

from django.contrib import admin
from .models import Currency, ExchangeRate, Payment, Transaction


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


# ─────────────────────────────────────────────────────────────────────────────
# TRANSACTION (inline for Payment)
# ─────────────────────────────────────────────────────────────────────────────

class TransactionInline(admin.TabularInline):
    """Show all transactions for a payment right inside the Payment detail page."""
    model   = Transaction
    extra   = 0
    readonly_fields = ("event_type", "transaction_date", "notes")
    can_delete = False


# ─────────────────────────────────────────────────────────────────────────────
# PAYMENT
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = (
        "id", "order_id", "payment_method", "payment_status",
        "amount_in_currency", "currency", "amount_in_usd", "created_at"
    )
    list_filter   = ("payment_status", "payment_method", "currency")
    search_fields = ("order_id", "reference_number")
    ordering      = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    inlines       = [TransactionInline]


# ─────────────────────────────────────────────────────────────────────────────
# TRANSACTION
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display  = ("id", "payment", "event_type", "transaction_date")
    list_filter   = ("event_type",)
    ordering      = ("-transaction_date",)
    readonly_fields = ("payment", "event_type", "transaction_date", "notes")

    def has_add_permission(self, request):
        # Transactions should only be created programmatically, not manually
        return False
