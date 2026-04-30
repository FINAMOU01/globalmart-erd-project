#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from products.models import Category, Product
from users.models import CustomUser

print("=" * 60)
print("DATABASE DIAGNOSTICS")
print("=" * 60)

try:
    print("\nUsers count:", CustomUser.objects.count())
except Exception as e:
    print(f"Error querying users: {e}")

try:
    print("Categories count:", Category.objects.count())
    print("First 5 categories:")
    for cat in Category.objects.all()[:5]:
        print(f"  - {cat.category_id}: {cat.name}")
except Exception as e:
    print(f"Error querying categories: {e}")

try:
    print("\nProducts count:", Product.objects.count())
    print("First 5 products:")
    for prod in Product.objects.all()[:5]:
        print(f"  - {prod.product_id}: {prod.name}")
except Exception as e:
    print(f"Error querying products: {e}")

print("\n" + "=" * 60)
print("END OF DIAGNOSTICS")
print("=" * 60)
