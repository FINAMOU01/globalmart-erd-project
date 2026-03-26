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

    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="exchange_rates",
        help_text="The currency this rate applies to"
    )
    rate_to_usd = models.DecimalField(
        max_digits=18,
        decimal_places=8,
        help_text="Value of 1 unit of this currency expressed in USD"
    )
    date_updated = models.DateTimeField(
        default=timezone.now,
        help_text="When this rate was recorded"
    )

    class Meta:
        verbose_name = "Exchange Rate"
        verbose_name_plural = "Exchange Rates"
        ordering = ["-date_updated"]
        # Enforce one rate per currency per datetime
        unique_together = [("currency", "date_updated")]

    def __str__(self):
        return f"1 {self.currency.currency_code} = {self.rate_to_usd} USD ({self.date_updated.date()})"


# ─────────────────────────────────────────────────────────────────────────────
# PAYMENT
# ─────────────────────────────────────────────────────────────────────────────

class Payment(models.Model):
    """
    One Payment record per order.

    Links an order (by order_id integer reference – Randy's model owns the
    Order table, we store just the ID to stay decoupled) to a payment attempt.

    Stores:
        - The amount the customer paid in their chosen currency
        - The equivalent amount in USD for accounting
        - The method used (card, mobile money, bank transfer, etc.)
        - The current payment status
    """

    # ── Payment method choices ────────────────────────────────────────────────
    METHOD_CARD = "CARD"
    METHOD_MOBILE_MONEY = "MOBILE_MONEY"
    METHOD_BANK_TRANSFER = "BANK_TRANSFER"
    METHOD_CASH_ON_DELIVERY = "CASH_ON_DELIVERY"

    PAYMENT_METHOD_CHOICES = [
        (METHOD_CARD, "Credit / Debit Card"),
        (METHOD_MOBILE_MONEY, "Mobile Money (MTN, Orange, M-Pesa)"),
        (METHOD_BANK_TRANSFER, "Bank Transfer"),
        (METHOD_CASH_ON_DELIVERY, "Cash on Delivery"),
    ]

    # ── Status choices ────────────────────────────────────────────────────────
    STATUS_PENDING = "PENDING"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_FAILED = "FAILED"
    STATUS_REFUNDED = "REFUNDED"

    PAYMENT_STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
        (STATUS_REFUNDED, "Refunded"),
    ]

    # ── Fields ────────────────────────────────────────────────────────────────

    # We reference Randy's order by ID only (loose coupling across branches)
    order_id = models.IntegerField(
        help_text="ID of the order being paid (from Randy's orders.Order model)"
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        help_text="Currency the customer chose at checkout"
    )
    amount_in_currency = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        help_text="Amount the customer paid in their chosen currency"
    )
    amount_in_usd = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        help_text="Equivalent amount in USD for reporting (computed at payment time)"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default=METHOD_CARD
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default=STATUS_PENDING
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the payment was initiated"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last status update"
    )

    # Optional: store a reference number (from a real payment gateway in future)
    reference_number = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="External reference (e.g. from payment gateway)"
    )

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Payment #{self.pk} | Order #{self.order_id} | "
            f"{self.amount_in_currency} {self.currency_id} | {self.payment_status}"
        )

    def mark_completed(self, reference=""):
        """Helper to mark a payment as completed and record the reference."""
        self.payment_status = self.STATUS_COMPLETED
        if reference:
            self.reference_number = reference
        self.save()

    def mark_failed(self):
        """Helper to mark a payment as failed."""
        self.payment_status = self.STATUS_FAILED
        self.save()


# ─────────────────────────────────────────────────────────────────────────────
# TRANSACTION
# ─────────────────────────────────────────────────────────────────────────────

class Transaction(models.Model):
    """
    An immutable audit-log entry for every payment event.

    Each time a Payment's status changes (or a payment attempt is made),
    a new Transaction row is written.  We never update or delete Transaction
    rows – this is the history of what happened.

    event_type choices:
        INITIATED  – customer clicked "Pay Now"
        SUCCESS    – payment gateway confirmed success
        FAILED     – gateway or validation failure
        REFUNDED   – refund issued
    """

    EVENT_INITIATED = "INITIATED"
    EVENT_SUCCESS = "SUCCESS"
    EVENT_FAILED = "FAILED"
    EVENT_REFUNDED = "REFUNDED"

    EVENT_TYPE_CHOICES = [
        (EVENT_INITIATED, "Initiated"),
        (EVENT_SUCCESS, "Success"),
        (EVENT_FAILED, "Failed"),
        (EVENT_REFUNDED, "Refunded"),
    ]

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="transactions",
        help_text="The payment this event belongs to"
    )
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        help_text="What kind of event occurred"
    )
    transaction_date = models.DateTimeField(
        default=timezone.now,
        help_text="When this event occurred"
    )
    notes = models.TextField(
        blank=True,
        default="",
        help_text="Additional info (error messages, gateway response, etc.)"
    )

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-transaction_date"]

    def __str__(self):
        return (
            f"Tx #{self.pk} | Payment #{self.payment_id} | "
            f"{self.event_type} @ {self.transaction_date.strftime('%Y-%m-%d %H:%M')}"
        )
