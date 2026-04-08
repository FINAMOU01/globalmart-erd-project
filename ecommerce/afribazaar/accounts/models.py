from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

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
    CURRENCY_CHOICES = [
        ('USD', 'USD - US Dollar'),
        ('EUR', 'EUR - Euro'),
        ('GBP', 'GBP - British Pound'),
        ('XAF', 'XAF - CFA Franc (Central)'),
        ('NGN', 'NGN - Nigerian Naira'),
        ('GHS', 'GHS - Ghanaian Cedi'),
        ('KES', 'KES - Kenyan Shilling'),
        ('ZAR', 'ZAR - South African Rand'),
        ('EGP', 'EGP - Egyptian Pound'),
        ('MAD', 'MAD - Moroccan Dirham'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    bio = models.TextField(blank=True, help_text="Description of your artisan work and experience")
    profile_picture = models.ImageField(upload_to='artisans/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    currency_preference = models.CharField(
        max_length=3,
        default='USD',
        choices=CURRENCY_CHOICES,
        help_text="Your default currency for displaying dashboard values"
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Artisan Profile"
    
    def get_average_rating(self):
        """Calculate average rating for this artisan"""
        from products.models import ArtisanRating
        ratings = ArtisanRating.objects.filter(artisan=self.user)
        if ratings.exists():
            return round(sum([r.rating for r in ratings]) / ratings.count(), 1)
        return 0
    
    def get_total_ratings(self):
        """Get total number of ratings"""
        from products.models import ArtisanRating
        return ArtisanRating.objects.filter(artisan=self.user).count()


class Wallet(models.Model):
    """Artisan wallet for storing balance and tracking earnings"""
    artisan = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.artisan.username}'s Wallet - Balance: {self.balance}"

    class Meta:
        verbose_name = "Artisan Wallet"
        verbose_name_plural = "Artisan Wallets"


class Transaction(models.Model):
    """Transaction history for wallet movements"""
    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255, blank=True, help_text="Transaction description (e.g., Sale, Withdrawal)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet.artisan.username} - {self.type.upper()} {self.amount} on {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
