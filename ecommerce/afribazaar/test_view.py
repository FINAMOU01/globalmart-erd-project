#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from products.views import ProductListView

# Create a request factory
factory = RequestFactory()

# Create a GET request to /products/shop/
request = factory.get('/products/shop/')
request.user = AnonymousUser()
request.session = {}

# Try to get the view
print("Testing ProductListView...")
try:
    view = ProductListView.as_view()
    print("View created successfully")
    
    print("Attempting to get context...")
    # We'll test the get_context_data method instead
    list_view = ProductListView()
    list_view.request = request
    list_view.paginate_by = 12
    
    # Get the queryset
    queryset = list_view.get_queryset()
    print(f"Queryset: {queryset.count()} products")
    
    # Get the context
    context = list_view.get_context_data()
    print(f"Categories: {context.get('categories', {}).count() if hasattr(context.get('categories', {}), 'count') else 'N/A'}")
    
    print("✓ View works fine")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
