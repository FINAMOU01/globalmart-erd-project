"""
Fix existing artisan accounts that don't have is_artisan flag set.
Run this script after deploying the fix.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def fix_artisan_flags():
    """Fix is_artisan flag for all artisans"""
    
    # Get all artisans with role='artisan' but is_artisan=False
    artisans_to_fix = User.objects.filter(role='artisan', is_artisan=False)
    
    if not artisans_to_fix.exists():
        print("✅ All artisans already have is_artisan=True")
        return
    
    count = artisans_to_fix.count()
    print(f"Found {count} artisans to fix...")
    
    for user in artisans_to_fix:
        user.is_artisan = True
        user.save()
        print(f"  ✓ Fixed: {user.username}")
    
    print(f"\n✅ Fixed {count} artisan accounts!")
    
    # Verify all customers have is_artisan=False
    customers_with_flag = User.objects.filter(role='customer', is_artisan=True)
    if customers_with_flag.exists():
        print(f"\nFixing {customers_with_flag.count()} customers with incorrect flag...")
        for user in customers_with_flag:
            user.is_artisan = False
            user.save()
            print(f"  ✓ Fixed: {user.username}")
    
    print("\n✅ All user flags are now consistent!")

if __name__ == '__main__':
    fix_artisan_flags()
