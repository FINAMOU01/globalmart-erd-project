"""
Test script to create sample orders for testing artisan dashboard
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from django.contrib.auth import get_user_model
from products.models import Product, Category
from orders.models import Order, OrderItem

User = get_user_model()

def create_test_data():
    """Create sample orders to test artisan dashboard"""
    
    # Get or create a customer
    customer, created = User.objects.get_or_create(
        username='testcustomer',
        defaults={
            'email': 'customer@test.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '+1234567890',
            'country': 'USA',
            'is_artisan': False,
        }
    )
    if created:
        customer.set_password('testpass123')
        customer.save()
    print(f"✓ Customer: {customer.username}")
    
    # Get an artisan
    artisan = User.objects.filter(is_artisan=True).first()
    if not artisan:
        print("⚠ No artisans found. Create an artisan account first.")
        return
    print(f"✓ Artisan: {artisan.username}")
    
    # Get products by the artisan
    products = Product.objects.filter(artisan=artisan)[:2]
    if not products:
        print("⚠ No products found for artisan. Create products first.")
        return
    print(f"✓ Found {products.count()} products")
    
    # Create an order
    order = Order.objects.create(
        customer=customer,
        status='confirmed',
        total_price=0,  # Will be calculated
    )
    print(f"✓ Created Order #{order.id}")
    
    # Create order items
    total = 0
    for product in products:
        quantity = 2
        item_total = product.price * quantity
        total += item_total
        
        OrderItem.objects.create(
            order=order,
            product=product,
            artisan=artisan,
            quantity=quantity,
            price=product.price,
        )
        print(f"  - Added {product.name} x{quantity} (USD {item_total})")
    
    # Update order total
    order.total_price = total
    order.save()
    print(f"✓ Order total: USD {total}")
    
    print("\n✅ Test data created successfully!")
    print(f"Visit http://127.0.0.1:8000/products/artisan/orders/ to view artisan orders")
    print(f"(Login as artisan first: {artisan.username})")

if __name__ == '__main__':
    create_test_data()
