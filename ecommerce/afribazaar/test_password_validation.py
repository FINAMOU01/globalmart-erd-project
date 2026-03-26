#!/usr/bin/env python
"""Test script to verify password similar to username is now allowed"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from accounts.forms import CustomerRegisterForm, ArtisanRegisterForm

# Test 1: Customer registration with password similar to username
print("=" * 60)
print("TEST 1: Customer Registration")
print("=" * 60)

customer_data = {
    'username': 'testuser123',
    'email': 'customer@example.com',
    'phone': '1234567890',
    'address': '123 Test Street',
    'password1': 'testuser123',  # Same as username
    'password2': 'testuser123',
}

customer_form = CustomerRegisterForm(data=customer_data)
if customer_form.is_valid():
    print("✅ PASS: Customer form accepts password similar to username")
    print(f"   Username: {customer_data['username']}")
    print(f"   Password: {customer_data['password1']}")
else:
    print("❌ FAIL: Customer form rejected the password")
    for field, errors in customer_form.errors.items():
        print(f"   {field}: {errors}")

# Test 2: Artisan registration with password similar to username
print("\n" + "=" * 60)
print("TEST 2: Artisan Registration")
print("=" * 60)

artisan_data = {
    'username': 'artisan456',
    'email': 'artisan@example.com',
    'phone': '9876543210',
    'address': '456 Artisan Road',
    'password1': 'artisan456',  # Same as username
    'password2': 'artisan456',
}

artisan_form = ArtisanRegisterForm(data=artisan_data)
if artisan_form.is_valid():
    print("✅ PASS: Artisan form accepts password similar to username")
    print(f"   Username: {artisan_data['username']}")
    print(f"   Password: {artisan_data['password1']}")
else:
    print("❌ FAIL: Artisan form rejected the password")
    for field, errors in artisan_form.errors.items():
        print(f"   {field}: {errors}")

# Test 3: Verify mismatched passwords are still rejected
print("\n" + "=" * 60)
print("TEST 3: Mismatched Passwords (Should be rejected)")
print("=" * 60)

mismatch_data = {
    'username': 'testuser789',
    'email': 'test@example.com',
    'phone': '5555555555',
    'address': '789 Test Ave',
    'password1': 'password123',
    'password2': 'password456',  # Different password
}

mismatch_form = CustomerRegisterForm(data=mismatch_data)
if not mismatch_form.is_valid():
    print("✅ PASS: Form correctly rejects mismatched passwords")
    for field, errors in mismatch_form.errors.items():
        print(f"   {field}: {errors}")
else:
    print("❌ FAIL: Form should reject mismatched passwords")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
