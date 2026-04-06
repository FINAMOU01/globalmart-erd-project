#!/usr/bin/env python
"""
Test le endpoint API de conversion de devises
"""

import os
import sys
import django
import json
from decimal import Decimal

sys.path.insert(0, r'c:\Users\finamou\Desktop\globalmart-erd-project\ecommerce\afribazaar')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from django.test import Client
from payments.models import Currency, ExchangeRate

print("=" * 70)
print(" Testing Currency Conversion API")
print("=" * 70)

# Test 1: Check currencies
print("\n✓ Test 1: Checking available currencies...")
currencies = Currency.objects.filter(is_active=True)
print(f"  Found {currencies.count()} active currencies:")
for curr in currencies[:5]:
    print(f"    - {curr.currency_code} ({curr.symbol})")
print(f"    ... and {max(0, currencies.count() - 5)} more")

# Test 2: Check exchange rates
print("\n✓ Test 2: Checking exchange rates...")
rates = ExchangeRate.objects.all()[:5]
for rate in rates:
    print(f"    - 1 {rate.currency} = {rate.rate_to_usd} USD")

# Test 3: Call API endpoints
print("\n✓ Test 3: Testing API conversion endpoints...")
client = Client()

test_cases = [
    {'from': 'USD', 'to': 'EUR', 'amount': 100},
    {'from': 'USD', 'to': 'NGN', 'amount': 100},
    {'from': 'USD', 'to': 'XAF', 'amount': 100},
    {'from': 'USD', 'to': 'ZAR', 'amount': 100},
]

for test in test_cases:
    url = f"/payments/api/convert/?from={test['from']}&to={test['to']}&amount={test['amount']}"
    print(f"\n  GET {url}")
    
    response = client.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"    ✓ {test['amount']} {test['from']} = {data.get('amount')} {test['to']}")
            print(f"      Symbol: {data.get('symbol')}")
            print(f"      Rate: {data.get('rate')}")
            print(f"      Formatted: {data.get('formatted')}")
        else:
            print(f"    ✗ Error: {data.get('error')}")
    else:
        print(f"    ✗ HTTP {response.status_code}")
        print(f"      Response: {response.content.decode()[:200]}")

print("\n" + "=" * 70)
print(" API Testing Complete!")
print("=" * 70)
print("\nNext: Start server and test payment form:")
print("  python manage.py runserver")
print("  http://localhost:8000/payments/pay/")
print("=" * 70)
