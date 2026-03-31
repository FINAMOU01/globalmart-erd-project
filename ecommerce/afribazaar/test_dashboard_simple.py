import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from django.test import Client
from accounts.models import ArtisanProfile

client = Client()
print("Testing Artisan Dashboard:")
print("="*60)

# Get an artisan user
try:
    artisan_profile = ArtisanProfile.objects.first()
    artisan = artisan_profile.user
    print(f"Artisan: {artisan.username}")
    print(f"Currency Preference: {artisan_profile.currency_preference}")
    print()
    
    # Login as artisan
    client.force_login(artisan)
    
    # Request dashboard
    response = client.get('/products/artisan/dashboard/', HTTP_HOST='127.0.0.1:8000')
    
    print(f"Dashboard Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ Dashboard rendered successfully!")
        print("\nContext Check:")
        if hasattr(response, 'context') and response.context:
            ctx = response.context
            if isinstance(ctx, list):
                ctx = ctx[0] if ctx else {}
            print(f"  - artisan_currency: {ctx.get('artisan_currency', 'NOT FOUND')}")
            print(f"  - currency_symbol: {ctx.get('currency_symbol', 'NOT FOUND')}")
            print(f"  - total_value: {ctx.get('total_value', 'NOT FOUND')}")
            print(f"  - total_sales: {ctx.get('total_sales', 'NOT FOUND')}")
        else:
            print("  Context not available in test response (this is normal for some view configurations)")
    else:
        print(f"✗ Dashboard returned {response.status_code}")
        print(response.content.decode()[:500])
        
except Exception as e:
    print(f"Error: {e}")
