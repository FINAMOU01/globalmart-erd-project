"""
AfriBazaar – Payment & Currency System
Module Owner: NOUDOU

tests.py – Unit tests for models, utilities, and views.

Run with:
    python manage.py test payments
"""

from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import Currency, ExchangeRate, Payment, Transaction
from .utils import convert_to_usd, convert_from_usd, get_latest_rate, format_amount


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: create test fixtures
# ─────────────────────────────────────────────────────────────────────────────

def create_test_currencies():
    """Create a minimal set of Currency + ExchangeRate rows for testing."""
    usd = Currency.objects.create(currency_code="USD", currency_name="US Dollar",
                                   symbol="$", is_active=True)
    xaf = Currency.objects.create(currency_code="XAF", currency_name="CFA Franc",
                                   symbol="FCFA", is_active=True)
    eur = Currency.objects.create(currency_code="EUR", currency_name="Euro",
                                   symbol="€", is_active=True)

    # 1 USD = 1.00 USD
    ExchangeRate.objects.create(currency=usd, rate_to_usd=Decimal("1.0"),
                                 date_updated=timezone.now())
    # 1 XAF = 0.0017 USD  →  1 USD ≈ 588 XAF
    ExchangeRate.objects.create(currency=xaf, rate_to_usd=Decimal("0.0017"),
                                 date_updated=timezone.now())
    # 1 EUR = 1.08 USD
    ExchangeRate.objects.create(currency=eur, rate_to_usd=Decimal("1.08"),
                                 date_updated=timezone.now())
    return usd, xaf, eur


# ─────────────────────────────────────────────────────────────────────────────
# MODEL TESTS
# ─────────────────────────────────────────────────────────────────────────────

class CurrencyModelTest(TestCase):

    def test_currency_str(self):
        c = Currency(currency_code="NGN", currency_name="Nigerian Naira", symbol="₦")
        self.assertIn("NGN", str(c))
        self.assertIn("₦", str(c))

    def test_currency_primary_key_is_code(self):
        Currency.objects.create(currency_code="GHS", currency_name="Cedi", symbol="₵")
        obj = Currency.objects.get(pk="GHS")
        self.assertEqual(obj.currency_name, "Cedi")


class ExchangeRateModelTest(TestCase):

    def setUp(self):
        self.usd, self.xaf, self.eur = create_test_currencies()

    def test_rate_str_includes_code(self):
        rate = ExchangeRate.objects.filter(currency=self.xaf).first()
        self.assertIn("XAF", str(rate))

    def test_latest_rate_returned(self):
        # Add a newer rate for XAF and verify get_latest_rate returns it
        newer_rate = Decimal("0.0020")
        ExchangeRate.objects.create(currency=self.xaf, rate_to_usd=newer_rate,
                                     date_updated=timezone.now())
        result = get_latest_rate("XAF")
        self.assertEqual(result.rate_to_usd, newer_rate)


class PaymentModelTest(TestCase):

    def setUp(self):
        self.usd, self.xaf, _ = create_test_currencies()

    def test_create_payment(self):
        payment = Payment.objects.create(
            order_id=42,
            currency=self.xaf,
            amount_in_currency=Decimal("5000.00"),
            amount_in_usd=Decimal("8.50"),
            payment_method=Payment.METHOD_MOBILE_MONEY,
        )
        self.assertEqual(payment.payment_status, Payment.STATUS_PENDING)

    def test_mark_completed(self):
        payment = Payment.objects.create(
            order_id=1, currency=self.usd,
            amount_in_currency=Decimal("20.00"),
            amount_in_usd=Decimal("20.00"),
        )
        payment.mark_completed(reference="TEST-REF")
        self.assertEqual(payment.payment_status, Payment.STATUS_COMPLETED)
        self.assertEqual(payment.reference_number, "TEST-REF")

    def test_mark_failed(self):
        payment = Payment.objects.create(
            order_id=2, currency=self.usd,
            amount_in_currency=Decimal("15.00"),
            amount_in_usd=Decimal("15.00"),
        )
        payment.mark_failed()
        self.assertEqual(payment.payment_status, Payment.STATUS_FAILED)

    def test_transaction_logged(self):
        payment = Payment.objects.create(
            order_id=3, currency=self.usd,
            amount_in_currency=Decimal("10.00"),
            amount_in_usd=Decimal("10.00"),
        )
        Transaction.objects.create(payment=payment, event_type=Transaction.EVENT_INITIATED)
        Transaction.objects.create(payment=payment, event_type=Transaction.EVENT_SUCCESS)
        self.assertEqual(payment.transactions.count(), 2)


# ─────────────────────────────────────────────────────────────────────────────
# UTILITY TESTS
# ─────────────────────────────────────────────────────────────────────────────

class UtilsTest(TestCase):

    def setUp(self):
        create_test_currencies()

    def test_convert_usd_to_usd(self):
        result = convert_to_usd(Decimal("10.00"), "USD")
        self.assertEqual(result, Decimal("10.00"))

    def test_convert_xaf_to_usd(self):
        # 1 XAF = 0.0017 USD, so 1000 XAF ≈ 1.70 USD
        result = convert_to_usd(Decimal("1000"), "XAF")
        self.assertAlmostEqual(float(result), 1.70, places=1)

    def test_convert_usd_to_xaf(self):
        # 1 USD / 0.0017 ≈ 588 XAF
        result = convert_from_usd(Decimal("1.00"), "XAF")
        self.assertGreater(result, Decimal("500"))

    def test_format_amount(self):
        usd = Currency.objects.get(pk="USD")
        formatted = format_amount(Decimal("1500.50"), usd)
        self.assertIn("1,500.50", formatted)
        self.assertIn("$", formatted)

    def test_get_latest_rate_missing(self):
        result = get_latest_rate("ZZZ")  # does not exist
        self.assertIsNone(result)


# ─────────────────────────────────────────────────────────────────────────────
# VIEW TESTS
# ─────────────────────────────────────────────────────────────────────────────

class PaymentViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        create_test_currencies()

    def test_payment_page_get(self):
        response = self.client.get(reverse("payments:payment_page"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AfriBazaar")

    def test_currency_rates_page(self):
        response = self.client.get(reverse("payments:currency_rates"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "USD")
        self.assertContains(response, "XAF")

    def test_api_convert_usd_to_xaf(self):
        url = reverse("payments:api_convert")
        response = self.client.get(url, {"amount": "10", "from": "USD", "to": "XAF"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("formatted", data)

    def test_api_convert_invalid_amount(self):
        url = reverse("payments:api_convert")
        response = self.client.get(url, {"amount": "abc", "from": "USD", "to": "XAF"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["success"])

    def test_set_currency_post(self):
        response = self.client.post(
            reverse("payments:set_currency"),
            {"currency_code": "XAF", "next": "/"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get("selected_currency"), "XAF")

    def test_payment_post_card(self):
        """Test a full card payment POST flow."""
        response = self.client.post(
            reverse("payments:payment_page"),
            {
                "order_id": "99",
                "currency_code": "USD",
                "payment_method": "CARD",
                "cardholder_name": "Test User",
                "card_last_four": "4242",
                "mobile_number": "",
            },
        )
        # Should redirect to confirmation
        self.assertEqual(response.status_code, 302)
        self.assertIn("confirmation", response["Location"])

    def test_payment_confirmation_page(self):
        """Confirmation page loads even with no payment in session."""
        response = self.client.get(reverse("payments:payment_confirmation"))
        self.assertEqual(response.status_code, 200)

    def test_payment_failed_page(self):
        response = self.client.get(reverse("payments:payment_failed"))
        self.assertEqual(response.status_code, 200)
