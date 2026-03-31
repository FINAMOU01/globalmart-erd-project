#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
sys.path.insert(0, '/root')
django.setup()

from orders.models import Order, OrderItem

# Fix all orders that have total_price = 0
orders_to_fix = Order.objects.filter(total_price=0)
print(f"Found {orders_to_fix.count()} orders with total_price = 0\n")

for order in orders_to_fix:
    total = sum(item.price * item.quantity for item in order.items.all())
    order.total_price = total
    order.save()
    print(f"✓ Order #{order.id}: Updated total to USD {total}")

print(f"\n{'='*50}")
print("All orders summary:")
print(f"{'='*50}\n")

all_orders = Order.objects.all().order_by('id')
for order in all_orders:
    status_color = "✓ Confirmed" if order.status == "confirmed" else f"⏳ {order.status.title()}"
    print(f"Order #{order.id}: {status_color:20s} | Total: USD {order.total_price:8.2f} | Items: {order.items.count()}")

print(f"\nDone!")
