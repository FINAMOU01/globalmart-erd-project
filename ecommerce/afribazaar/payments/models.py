"""
AfriBazaar – Payment & Currency System
Module Owner: NOUDOU

This file defines all database models for the Payment and Currency module.

Models:
    - Currency        : Supported currencies (USD, EUR, XAF, NGN, GHS, KES, ZAR)
    - ExchangeRate    : Rate of each currency relative to USD (base currency)
    - Payment         : One payment record per order
    - Transaction     : Audit trail of every payment event (initiated, success, failed)
"""

from django.db import models
from django.utils import timezone


# ─────────────────────────────────────────────────────────────────────────────
# CURRENCY
# ─────────────────────────────────────────────────────────────────────────────

class Currency(models.Model):
    """
    Represents a currency supported by AfriBazaar.
    currency_code is the ISO 4217 3-letter code and serves as the primary key.

    Examples: USD, EUR, XAF (CFA Franc), NGN (Naira), GHS (Cedi), KES (Shilling)
    """

    currency_code = models.CharField(
        max_length=3,
        primary_key=True,
        help_text="ISO 4217 code, e.g. USD, XAF, NGN"
    )
    currency_name = models.CharField(
        max_length=100,
        help_text="Full name, e.g. US Dollar, CFA Franc"
    )
    symbol = models.CharField(
        max_length=10,
        db_column='currency_symbol',
        help_text="Display symbol, e.g. $, €, ₦, FCFA"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="If False, this currency is hidden from the selector"
    )

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        ordering = ["currency_code"]
        db_table = 'currencies'
        managed = False

    def __str__(self):
        return f"{self.currency_code} – {self.currency_name} ({self.symbol})"


# ─────────────────────────────────────────────────────────────────────────────
# EXCHANGE RATE
# ─────────────────────────────────────────────────────────────────────────────

class ExchangeRate(models.Model):
    """
    Stores the exchange rate of a currency relative to USD (base currency).

    rate_to_usd = how many USD equals 1 unit of this currency.
    Example: For XAF (CFA Franc), 1 XAF ≈ 0.00165 USD  →  rate_to_usd = 0.00165
             For EUR, 1 EUR ≈ 1.08 USD                  →  rate_to_usd = 1.08

    We keep historical records (one row per currency per update date).
    The latest entry for a currency is used for conversion.
    """
    exchange_rate_id = models.AutoField(primary_key=True, db_column='exchange_rate_id')
    
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="exchange_rates",
        db_column='currency_code',
        help_text="The currency this rate applies to"
    )
    rate_to_usd = models.DecimalField(
        max_digits=18,
        decimal_places=8,
        help_text="Value of 1 unit of this currency expressed in USD"
    )
    date_updated = models.DateTimeField(
        default=timezone.now,
        db_column='effective_date',
        help_text="When this rate was recorded"
    )

    class Meta:
        verbose_name = "Exchange Rate"
        verbose_name_plural = "Exchange Rates"
        ordering = ["-date_updated"]
        # Enforce one rate per currency per datetime
        unique_together = [("currency", "date_updated")]
        db_table = 'exchange_rates'
        managed = False

    def __str__(self):
        return f"1 {self.currency.currency_code} = {self.rate_to_usd} USD ({self.date_updated.date()})"
