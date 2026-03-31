import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from products.models import Product
from payments.models import Currency, ExchangeRate
from orders.models import Order

print("Database Check - Post Load")
print("=" * 60)

print(f"\nProducts: {Product.objects.count()}")
print(f"Currencies: {Currency.objects.count()}")
print(f"Exchange Rates: {ExchangeRate.objects.count()}")

if Product.objects.count() > 0:
    products = Product.objects.all()[:3]
    print("\nSample Products:")
    for p in products:
        print(f"  - {p.name}: {p.price} {p.currency_code}")
else:
    print("\n⚠️  No products found!")

if Currency.objects.count() > 0:
    currencies = Currency.objects.all()[:3]
    print("\nSample Currencies:")
    for c in currencies:
        print(f"  - {c.currency_code}: {c.symbol}")
else:
    print("\n⚠️  No currencies found!")
