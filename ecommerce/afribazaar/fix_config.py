#!/usr/bin/env python
"""
Fix configuration for accounts app
"""
import os

# Change to the Django project directory  
base_dir = os.path.dirname(os.path.abspath(__file__))

# 1. FIX settings.py - Add MEDIA configuration
settings_path = os.path.join(base_dir, 'afribazaar', 'settings.py')
with open(settings_path, 'r') as f:
    settings_content = f.read()

if 'MEDIA_URL' not in settings_content:
    old_static = """STATICFILES_DIRS = [
    BASE_DIR / 'static',
]"""
    new_static = """STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files (User uploads)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Login redirect
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'"""
    settings_content = settings_content.replace(old_static, new_static)
    
with open(settings_path, 'w') as f:
    f.write(settings_content)
print("✓ Fixed settings.py - Added MEDIA configuration")

# 2. FIX models.py - Remove duplicate signals
models_path = os.path.join(base_dir, 'accounts', 'models.py')
new_models = """from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Customer Profile"


class ArtisanProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Artisan Profile"
"""
with open(models_path, 'w') as f:
    f.write(new_models)
print("✓ Fixed models.py - Removed duplicate signals")

# 3. FIX admin.py - Register models
admin_path = os.path.join(base_dir, 'accounts', 'admin.py')
new_admin = """from django.contrib import admin
from .models import CustomerProfile, ArtisanProfile


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'date_joined')
    search_fields = ('user__username', 'phone')
    readonly_fields = ('date_joined',)
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'address')
        }),
        ('Profile Picture', {
            'fields': ('profile_picture',)
        }),
        ('Metadata', {
            'fields': ('date_joined',)
        }),
    )


@admin.register(ArtisanProfile)
class ArtisanProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_verified', 'date_joined')
    search_fields = ('user__username', 'phone')
    readonly_fields = ('date_joined',)
    list_filter = ('is_verified', 'date_joined')
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'address')
        }),
        ('Profile Picture', {
            'fields': ('profile_picture',)
        }),
        ('Verification Status', {
            'fields': ('is_verified',)
        }),
        ('Metadata', {
            'fields': ('date_joined',)
        }),
    )
"""
with open(admin_path, 'w') as f:
    f.write(new_admin)
print("✓ Fixed admin.py - Registered models")

print("\n✅ All backend configuration fixes complete!")
