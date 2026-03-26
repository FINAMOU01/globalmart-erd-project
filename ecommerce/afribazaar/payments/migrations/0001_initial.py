"""
Auto-generated migration for the payments app.
Handles: Currency, ExchangeRate, Payment, Transaction
"""

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        # ── Currency ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "currency_code",
                    models.CharField(
                        max_length=3,
                        primary_key=True,
                        serialize=False,
                        help_text="ISO 4217 code, e.g. USD, XAF, NGN",
                    ),
                ),
                (
                    "currency_name",
                    models.CharField(
                        max_length=100,
                        help_text="Full name, e.g. US Dollar, CFA Franc",
                    ),
                ),
                (
                    "symbol",
                    models.CharField(
                        max_length=10,
                        help_text="Display symbol, e.g. $, €, ₦, FCFA",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="If False, hidden from selector",
                    ),
                ),
            ],
            options={"verbose_name": "Currency", "verbose_name_plural": "Currencies", "ordering": ["currency_code"]},
        ),
        # ── ExchangeRate ──────────────────────────────────────────────────────
        migrations.CreateModel(
            name="ExchangeRate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                (
                    "currency",
                    models.ForeignKey(
                        help_text="The currency this rate applies to",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exchange_rates",
                        to="payments.currency",
                    ),
                ),
                (
                    "rate_to_usd",
                    models.DecimalField(
                        decimal_places=8,
                        max_digits=18,
                        help_text="Value of 1 unit of this currency in USD",
                    ),
                ),
                (
                    "date_updated",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="When this rate was recorded",
                    ),
                ),
            ],
            options={
                "verbose_name": "Exchange Rate",
                "verbose_name_plural": "Exchange Rates",
                "ordering": ["-date_updated"],
            },
        ),
        migrations.AddConstraint(
            model_name="exchangerate",
            constraint=models.UniqueConstraint(
                fields=["currency", "date_updated"], name="unique_currency_rate_per_date"
            ),
        ),
        # ── Payment ───────────────────────────────────────────────────────────
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("order_id", models.IntegerField(help_text="ID of the order being paid")),
                (
                    "currency",
                    models.ForeignKey(
                        help_text="Currency chosen at checkout",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="payments.currency",
                    ),
                ),
                ("amount_in_currency", models.DecimalField(decimal_places=2, max_digits=14)),
                ("amount_in_usd", models.DecimalField(decimal_places=2, max_digits=14)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("CARD", "Credit / Debit Card"),
                            ("MOBILE_MONEY", "Mobile Money (MTN, Orange, M-Pesa)"),
                            ("BANK_TRANSFER", "Bank Transfer"),
                            ("CASH_ON_DELIVERY", "Cash on Delivery"),
                        ],
                        default="CARD",
                        max_length=20,
                    ),
                ),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("COMPLETED", "Completed"),
                            ("FAILED", "Failed"),
                            ("REFUNDED", "Refunded"),
                        ],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("reference_number", models.CharField(blank=True, default="", max_length=100)),
            ],
            options={"verbose_name": "Payment", "verbose_name_plural": "Payments", "ordering": ["-created_at"]},
        ),
        # ── Transaction ───────────────────────────────────────────────────────
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                (
                    "payment",
                    models.ForeignKey(
                        help_text="The payment this event belongs to",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="payments.payment",
                    ),
                ),
                (
                    "event_type",
                    models.CharField(
                        choices=[
                            ("INITIATED", "Initiated"),
                            ("SUCCESS", "Success"),
                            ("FAILED", "Failed"),
                            ("REFUNDED", "Refunded"),
                        ],
                        max_length=20,
                    ),
                ),
                ("transaction_date", models.DateTimeField(default=django.utils.timezone.now)),
                ("notes", models.TextField(blank=True, default="")),
            ],
            options={"verbose_name": "Transaction", "verbose_name_plural": "Transactions", "ordering": ["-transaction_date"]},
        ),
    ]
