import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afribazaar.settings')
django.setup()

from accounts.models import ArtisanProfile
from users.models import CustomUser

# Get Artisan1
artisan = CustomUser.objects.filter(username='Artisan1').first()

if artisan:
    profile = artisan.artisanprofile
    # Set the profile picture to the existing file
    profile.profile_picture = 'artisans/portrait-black-african-man-standing-with-arm-crossed-black-people-concept_10257_dyRbILH.jpg'
    profile.save()
    print(f"✓ Updated {artisan.username}'s profile picture")
    print(f"  Profile picture: {profile.profile_picture}")
    print(f"  Profile picture URL: {profile.profile_picture.url}")
else:
    print("✗ Artisan1 not found")
