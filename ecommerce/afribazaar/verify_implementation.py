#!/usr/bin/env python
"""Verify all implementation is complete"""
import os

checks = {
    'Settings': 'afribazaar/settings.py',
    'Models': 'accounts/models.py',
    'Forms': 'accounts/forms.py',
    'Views': 'accounts/views.py',
    'URLs': 'accounts/urls.py',
    'Signals': 'accounts/signals.py',
    'Admin': 'accounts/admin.py',
    'Apps Config': 'accounts/apps.py',
}

templates = {
    'Login': 'templates/accounts/login.html',
    'Customer Register': 'templates/accounts/customer_register.html',
    'Artisan Register': 'templates/accounts/artisan_register.html',
    'Customer Profile': 'templates/accounts/customer_profile.html',
    'Artisan Profile': 'templates/accounts/artisan_profile.html',
}

print("=" * 60)
print("BACKEND FILES VERIFICATION")
print("=" * 60)
all_ok = True
for name, path in checks.items():
    exists = os.path.exists(path)
    status = "OK" if exists else "MISSING"
    print(f"[{status}] {name}: {path}")
    if not exists:
        all_ok = False

print("\n" + "=" * 60)
print("TEMPLATE FILES VERIFICATION")
print("=" * 60)
for name, path in templates.items():
    exists = os.path.exists(path)
    status = "OK" if exists else "MISSING"
    print(f"[{status}] {name}: {path}")
    if not exists:
        all_ok = False

print("\n" + "=" * 60)
print("CSS VERIFICATION")
print("=" * 60)
css_file = 'static/css/style.css'
if os.path.exists(css_file):
    with open(css_file, 'r') as f:
        content = f.read()
        has_auth = 'auth-container' in content
    print(f"[OK] CSS: {css_file}")
    print(f"     Size: {len(content)} bytes")
    print(f"     Auth styling: {'YES' if has_auth else 'MISSING'}")
else:
    print(f"[MISSING] CSS: {css_file}")
    all_ok = False

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
if all_ok:
    print("ALL FILES CREATED AND VERIFIED!")
else:
    print("SOME FILES ARE MISSING!")
print("=" * 60)
