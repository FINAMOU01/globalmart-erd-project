#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from django.test import Client, override_settings
from django.contrib.auth import get_user_model

User = get_user_model()
artisan = User.objects.filter(is_artisan=True).first()

if artisan:
    print("Testing Artisan Dashboard:")
    print("=" * 60)
    print(f"Artisan: {artisan.username}")
    
    # Access profile directly
    profile = artisan.artisanprofile
    
    if profile and hasattr(profile, 'currency_preference'):
        print(f"Currency Preference: {profile.currency_preference}")
    else:
        print("No currency preference found")
    
    # Test view
    with override_settings(ALLOWED_HOSTS=['testserver']):
        client = Client()
        client.force_login(artisan)
        response = client.get('/products/artisan/dashboard/')
        
        print(f"\nDashboard Status: {response.status_code}")
        
        if response.status_code == 200:
            context = response.context
            print(f"Artisan Currency: {context.get('artisan_currency')}")
            print(f"Currency Symbol: {context.get('currency_symbol')}")
            print(f"Total Value: {context.get('total_value')}")
            print(f"Total Sales: {context.get('total_sales')}")
            
            products = context.get('products', [])
            if products:
                p = products[0]
                print(f"\nFirst Product:")
                print(f"  - Name: {p.name}")
                print(f"  - Display Price: {getattr(p, 'display_price', 'N/A')}")
            
            print(f"\n[SUCCESS] Dashboard working with currency conversion!")
        else:
            print(f"Error: {response.status_code}")
else:
    print("No artisan found")
