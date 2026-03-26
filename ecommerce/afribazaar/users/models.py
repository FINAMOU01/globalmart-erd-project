from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator

class CustomUser(AbstractUser):
    """
    Extended User model for AfriBazaar.
    Extends Django's built-in User model.
    """
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('artisan', 'Artisan/Seller'),
    ]
    
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='customer',
        help_text="User role in the marketplace"
    )
    is_artisan = models.BooleanField(default=False, help_text="Is this user an artisan/seller?")
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    
    class Meta:
        ordering = ['-date_joined']


class ArtisanProfile(models.Model):
    """
    Profile for artisans/sellers on the marketplace.
    One-to-One relationship with CustomUser.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='artisan_profile')
    bio = models.TextField(blank=True, null=True, help_text="Short biography about the artisan")
    profile_image = models.ImageField(
        upload_to='artisans/', 
        blank=True, 
        null=True,
        help_text="Profile picture for the artisan"
    )
    social_links = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text='JSON format: {"instagram": "url", "facebook": "url", "twitter": "url"}'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Artisan Profile - {self.user.get_full_name()}"
    
    class Meta:
        ordering = ['-created_at']
