import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from accounts.models import ArtisanProfile
from products.models import Product
from payments.models import Currency, ExchangeRate

print("AfriBazaar Multi-Currency System Verification")
print("=" * 60)

# Check ArtisanProfile
print("\n1. ArtisanProfile:")
ap = ArtisanProfile.objects.first()
if ap:
    print(f"   Artisan: {ap.user.username}")
    print(f"   Currency Preference: {ap.currency_preference}")
    print(f"   Bio: {ap.bio[:50] if ap.bio else 'No bio'}")
else:
    print("   No ArtisanProfile found")

# Check Currency
print("\n2. Currency Support:")
currencies = Currency.objects.all()
print(f"   Total currencies: {currencies.count()}")
for c in currencies[:5]:
    print(f"     - {c.currency_code}: {c.currency_name} ({c.symbol})")

# Check ExchangeRate
print("\n3. Exchange Rates:")
rates = ExchangeRate.objects.all()
print(f"   Exchange rates available: {rates.count()}")
for r in rates[:5]:
    print(f"     - 1 {r.currency.currency_code} = {r.rate_to_usd} USD")

# Check Product
print("\n4. Sample Products:")
products = Product.objects.all()[:3]
for p in products:
    print(f"   - {p.name}: {p.price} {p.currency_code}")

print("\n✓ Verification Complete!")
