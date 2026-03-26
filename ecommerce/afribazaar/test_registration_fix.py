"""
Test to verify artisan and customer registration forms correctly set is_artisan flag
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from accounts.forms import ArtisanRegisterForm, CustomerRegisterForm
from django.contrib.auth import get_user_model

User = get_user_model()

def test_artisan_registration():
    """Test that ArtisanRegisterForm correctly sets is_artisan=True"""
    print("Testing Artisan Registration...")
    
    form_data = {
        'username': 'test_artisan_temp',
        'email': 'test_artisan@test.com',
        'phone': '+1234567890',
        'address': 'Test Address',
        'password1': 'testpass123',
        'password2': 'testpass123',
    }
    
    form = ArtisanRegisterForm(data=form_data)
    
    if form.is_valid():
        user = form.save()
        if user.role == 'artisan' and user.is_artisan:
            print("✅ PASS: Artisan form correctly sets role='artisan' and is_artisan=True")
        else:
            print(f"❌ FAIL: role={user.role}, is_artisan={user.is_artisan}")
        # Cleanup
        user.delete()
    else:
        print(f"❌ FAIL: Form errors: {form.errors}")

def test_customer_registration():
    """Test that CustomerRegisterForm correctly sets is_artisan=False"""
    print("Testing Customer Registration...")
    
    form_data = {
        'username': 'test_customer_temp',
        'email': 'test_customer@test.com',
        'phone': '+1234567890',
        'address': 'Test Address',
        'password1': 'testpass123',
        'password2': 'testpass123',
    }
    
    form = CustomerRegisterForm(data=form_data)
    
    if form.is_valid():
        user = form.save()
        if user.role == 'customer' and not user.is_artisan:
            print("✅ PASS: Customer form correctly sets role='customer' and is_artisan=False")
        else:
            print(f"❌ FAIL: role={user.role}, is_artisan={user.is_artisan}")
        # Cleanup
        user.delete()
    else:
        print(f"❌ FAIL: Form errors: {form.errors}")

if __name__ == '__main__':
    test_artisan_registration()
    test_customer_registration()
    print("\n✅ All registration tests completed!")
