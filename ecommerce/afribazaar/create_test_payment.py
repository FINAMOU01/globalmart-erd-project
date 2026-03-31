#!/usr/bin/env python
import os
import sys
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
sys.path.insert(0, '/root')
django.setup()

from orders.models import Order
from payments.models import Payment, Transaction, Currency

# Get order #2
order = Order.objects.get(id=2)

# Get USD currency
usd = Currency.objects.get(currency_code='USD')

print(f"Creating payment for Order #{order.id}...\n")

# Create payment record
payment = Payment.objects.create(
    order_id=order.id,
    currency=usd,
    amount_in_currency=Decimal('200000.00'),
    amount_in_usd=Decimal('200000.00'),
    payment_method=Payment.METHOD_CARD,
    payment_status=Payment.STATUS_COMPLETED,
    reference_number=f"AFRI-{100001:06d}"
)

print(f"✓ Payment created: #{payment.id}")
print(f"  Amount: {payment.currency.symbol} {payment.amount_in_currency}")
print(f"  Status: {payment.payment_status}")

# Create success transaction
trans = Transaction.objects.create(
    payment=payment,
    event_type=Transaction.EVENT_SUCCESS,
    notes="Simulated payment gateway: approved.",
)

print(f"✓ Transaction recorded: {trans.event_type}")

# Update order status
order.status = 'confirmed'
order.total_price = order.get_items_total()
order.save()

print(f"\n✓ Order #{order.id} updated:")
print(f"  Status: {order.status} (was: pending)")
print(f"  Total: USD {order.total_price}")

print(f"\nDone! Check your artisan dashboard now - the order should show as 'Confirmed'")
