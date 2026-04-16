#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import ArtisanProfile
from django.conf import settings

User = get_user_model()
artisan = User.objects.filter(email='artisan7@gmail.com').first()

if artisan:
    try:
        profile = artisan.artisanprofile
        print(f'✓ Artisan: {artisan.username}')
        print(f'✓ Profile exists')
        print(f'  Profile picture field: {profile.profile_picture}')
        print(f'  Profile picture name: {profile.profile_picture.name if profile.profile_picture else "None"}')
        
        # List files in media/artisans directory
        artisans_dir = os.path.join(settings.MEDIA_ROOT, 'artisans')
        if os.path.exists(artisans_dir):
            files = os.listdir(artisans_dir)
            print(f'  Files in media/artisans: {len(files)} files')
            for f in files[:5]:
                print(f'    - {f}')
    except Exception as e:
        print(f'✗ Error: {e}')
        import traceback
        traceback.print_exc()
else:
    print('✗ Artisan not found')
