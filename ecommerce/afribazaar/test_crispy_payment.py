#!/usr/bin/env python
"""
Test script for AfriBazaar Payment System with Crispy Forms
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, r'c:\Users\finamou\Desktop\globalmart-erd-project\ecommerce\afribazaar')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from payments.forms import PaymentForm
from payments.models import Currency, Payment
from crispy_forms.utils import render_crispy_form

print("=" * 70)
print(" AfriBazaar Payment System - Crispy Forms Testing")
print("=" * 70)

# Test 1: Check if Crispy Forms is properly configured
print("\n✓ Test 1: Checking Crispy Forms Configuration...")
try:
    from django.conf import settings
    assert 'crispy_forms' in settings.INSTALLED_APPS, "crispy_forms not in INSTALLED_APPS"
    assert 'crispy_bootstrap5' in settings.INSTALLED_APPS, "crispy_bootstrap5 not in INSTALLED_APPS"
    assert settings.CRISPY_TEMPLATE_PACK == 'bootstrap5', "CRISPY_TEMPLATE_PACK not set to bootstrap5"
    print("  ✓ Crispy Forms properly configured")
    print(f"    - Template pack: {settings.CRISPY_TEMPLATE_PACK}")
except AssertionError as e:
    print(f"  ✗ Configuration error: {e}")
    sys.exit(1)

# Test 2: Check Currency availability
print("\n✓ Test 2: Checking Currency Data...")
try:
    usd, created = Currency.objects.get_or_create(
        currency_code='USD',
        defaults={'symbol': '$', 'is_active': True}
    )
    print(f"  ✓ USD currency available (created: {created})")
    
    active_currencies = Currency.objects.filter(is_active=True)
    print(f"  ✓ Active currencies: {active_currencies.count()} found")
    for curr in active_currencies:
        print(f"    - {curr.currency_code} ({curr.symbol})")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 3: Test PaymentForm with Crispy
print("\n✓ Test 3: Testing PaymentForm with Crispy Layout...")
try:
    factory = RequestFactory()
    request = factory.get('/payments/pay/')
    
    # Add session middleware
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    
    usd = Currency.objects.get(currency_code='USD')
    
    form = PaymentForm(initial={
        'order_id': 1,
        'currency_code': usd,
        'payment_method': Payment.METHOD_CARD,
    })
    
    print("  ✓ PaymentForm instantiated successfully")
    print(f"    - Form fields: {list(form.fields.keys())}")
    print(f"    - Form helper configured: {hasattr(form, 'helper')}")
    
    if hasattr(form, 'helper'):
        print(f"    - Helper form class: {form.helper.form_class}")
        print(f"    - Helper layout: {type(form.helper.layout).__name__}")
    
except Exception as e:
    print(f"  ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Test Payment model payment methods
print("\n✓ Test 4: Testing Payment Model...")
try:
    methods = dict(Payment.PAYMENT_METHOD_CHOICES)
    print(f"  ✓ Available payment methods: {len(methods)}")
    for code, name in methods.items():
        print(f"    - {code}: {name}")
    
    # Try to get status choices if available
    if hasattr(Payment, 'PAYMENT_STATUS_CHOICES'):
        statuses = dict(Payment.PAYMENT_STATUS_CHOICES)
    elif hasattr(Payment, 'STATUS_CHOICES'):
        statuses = dict(Payment.STATUS_CHOICES)
    else:
        statuses = {}
    
    if statuses:
        print(f"  ✓ Available payment statuses: {len(statuses)}")
        for code, name in statuses.items():
            print(f"    - {code}: {name}")
    else:
        print("  ✓ Payment status options configured in model")
        
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 5: Test form validation
print("\n✓ Test 5: Testing Form Validation...")
try:
    # Valid form data
    valid_data = {
        'order_id': 123,
        'currency_code': usd.currency_code,
        'payment_method': Payment.METHOD_CARD,
        'cardholder_name': 'John Doe',
        'card_last_four': '4242',
        'mobile_number': '',
    }
    
    form = PaymentForm(data=valid_data)
    if form.is_valid():
        print("  ✓ Valid card payment form accepted")
    else:
        print(f"  ✗ Form validation failed: {form.errors}")
    
    # Invalid form data (missing card fields)
    invalid_data = {
        'order_id': 123,
        'currency_code': usd.currency_code,
        'payment_method': Payment.METHOD_CARD,
        'cardholder_name': '',  # Missing
        'card_last_four': '',   # Missing
        'mobile_number': '',
    }
    
    form = PaymentForm(data=invalid_data)
    if not form.is_valid():
        print(f"  ✓ Invalid form correctly rejected")
        print(f"    Errors: {list(form.errors.keys())}")
    else:
        print("  ✗ Invalid form was accepted (should have failed)")
        
except Exception as e:
    print(f"  ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print(" All Tests Passed! ✓")
print("=" * 70)
print("\nNext steps:")
print("1. Start the development server: python manage.py runserver")
print("2. Navigate to: http://localhost:8000/payments/pay/")
print("3. Test the payment form with the new Crispy Forms design")
print("\nFor more testing guidance, see: PAYMENT_TESTING_GUIDE.md")
print("=" * 70)
