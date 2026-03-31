#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
artisan = User.objects.filter(is_artisan=True).first()
if artisan:
    profile = artisan.artisanprofile
    print(f'Profile: {profile}')
    print(f'UUID Currency: {profile.currency_preference if hasattr(profile, "currency_preference") else "MISSING"}')
    print(f'SUCCESS!')
