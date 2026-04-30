from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Custom user manager for mapping to schema users table"""
    
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    """
    Custom User model mapped to schema 'users' table.
    Replaces Django's default auth_user table.
    """
    # Primary Key
    user_id = models.AutoField(primary_key=True, db_column='user_id')
    
    # Core fields
    username = models.CharField(max_length=50, unique=True, db_column='username')
    email = models.EmailField(unique=True, db_column='email')
    password = models.CharField(max_length=255, db_column='password_hash')
    
    # Profile fields
    first_name = models.CharField(max_length=100, blank=True, null=True, db_column='first_name')
    last_name = models.CharField(max_length=100, blank=True, null=True, db_column='last_name')
    phone_number = models.CharField(max_length=20, blank=True, null=True, db_column='phone_number')
    
    # Role fields
    is_artisan = models.BooleanField(default=False, db_column='is_artisan')
    is_admin = models.BooleanField(default=False, db_column='is_admin')
    is_active = models.BooleanField(default=True, db_column='is_active')
    
    # Account status
    account_status = models.CharField(
        max_length=20,
        default='active',
        choices=[
            ('active', 'Active'),
            ('suspended', 'Suspended'),
            ('deleted', 'Deleted'),
            ('pending_verification', 'Pending Verification'),
        ],
        db_column='account_status'
    )
    
    # Tier reference (FK to customer_tiers)
    tier_id = models.IntegerField(default=1, db_column='tier_id')
    
    # Email verification
    email_verified = models.BooleanField(default=False, db_column='email_verified')
    email_verified_at = models.DateTimeField(null=True, blank=True, db_column='email_verified_at')
    
    # Timestamps
    last_login = models.DateTimeField(null=True, blank=True, db_column='last_login')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')
    
    # Manager
    objects = CustomUserManager()
    
    # Django auth configuration
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    
    def get_full_name(self):
        """Return full name or username if name not set"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    class Meta:
        db_table = 'users'
        managed = False
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'


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
