#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from accounts.models import ArtisanProfile
from django.conf import settings

# Get one artisan with a profile picture
try:
    artisan = ArtisanProfile.objects.filter(profile_picture__isnull=False).first()
    if artisan:
        print(f"Found artisan: {artisan.user.username}")
        print(f"Profile picture field value: {artisan.profile_picture}")
        print(f"Profile picture URL: {artisan.profile_picture.url}")
        print(f"Profile picture path: {artisan.profile_picture.path}")
        print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
        print(f"MEDIA_URL: {settings.MEDIA_URL}")
        
        if os.path.exists(artisan.profile_picture.path):
            print(f"✓ File EXISTS at: {artisan.profile_picture.path}")
        else:
            print(f"✗ File NOT FOUND at: {artisan.profile_picture.path}")
    else:
        print("No artisans with profile pictures found")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
