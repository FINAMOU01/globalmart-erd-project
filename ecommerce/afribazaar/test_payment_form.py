#!/usr/bin/env python
"""
Test script to verify payment form and currencies are working correctly.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from payments.models import Currency, Payment
from payments.forms import PaymentForm
from django.contrib.auth import get_user_model

User = get_user_model()

print("="*80)
print("🔍 TESTING PAYMENT FORM AND CURRENCIES")
print("="*80)

# 1. Check if currencies exist
print("\n1️⃣  Checking currencies in database...")
currencies = Currency.objects.filter(is_active=True)
print(f"   Found {currencies.count()} active currencies:")
for curr in currencies:
    print(f"     - {curr.currency_code}: {curr.currency_name} (symbol: {curr.symbol})")

if not currencies.exists():
    print("   ❌ NO ACTIVE CURRENCIES FOUND!")
    print("   This is the problem! The form cannot work without currencies.")
else:
    print("   ✅ Currencies exist")

# 2. Test the form with valid data
print("\n2️⃣  Testing PaymentForm with valid data...")
test_data = {
    'order_id': 1,
    'currency_code': 'USD',  # Use the currency_code value
    'payment_method': 'CARD',
}

print(f"   Submitting test data: {test_data}")
form = PaymentForm(test_data)

if form.is_valid():
    print("   ✅ FORM VALID!")
    print(f"      Cleaned currency_code: {form.cleaned_data['currency_code']}")
    print(f"      Cleaned payment_method: {form.cleaned_data['payment_method']}")
else:
    print("   ❌ FORM INVALID!")
    print(f"      Form errors: {form.errors}")
    for field, errors in form.errors.items():
        print(f"        Field '{field}': {errors}")

# 3. Test currency lookup
print("\n3️⃣  Testing currency lookup...")
try:
    usd_currency = Currency.objects.get(currency_code='USD', is_active=True)
    print(f"   ✅ Found USD currency: {usd_currency}")
except Currency.DoesNotExist:
    print("   ❌ USD currency not found!")

# 4. Test payment method choices
print("\n4️⃣  Testing payment method choices...")
print(f"   Payment method choices:")
for code, label in Payment.PAYMENT_METHOD_CHOICES:
    print(f"     - {code}: {label}")

print("\n" + "="*80)
print("✅ TEST COMPLETE")
print("="*80)
