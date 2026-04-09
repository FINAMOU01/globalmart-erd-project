from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
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


class WithdrawalRequest(models.Model):
    """Withdrawal requests from artisans with auto-approval"""
    PAYMENT_METHODS = [
        ('bank_transfer', 'Bank Transfer'),
        ('mtn', 'MTN Mobile Money'),
        ('orange', 'Orange Money'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Processing'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    MINIMUM_WITHDRAWAL = Decimal('10.00')  # Minimum $10
    WITHDRAWAL_TAX_PERCENTAGE = Decimal('5.00')  # 5% tax to admin
    
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawal_requests')
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='withdrawals')
    amount_requested = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    bank_account_name = models.CharField(max_length=255, blank=True, help_text="For bank transfer")
    bank_account_number = models.CharField(max_length=50, blank=True, help_text="For bank transfer")
    mobile_number = models.CharField(max_length=20, blank=True, help_text="For MTN/Orange Money")
    
    # Tax calculation
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    amount_after_tax = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.artisan.username} - {self.amount_requested} ({self.get_status_display()})"
    
    def calculate_taxes(self):
        """Calculate tax on withdrawal amount"""
        self.tax_amount = self.amount_requested * (self.WITHDRAWAL_TAX_PERCENTAGE / Decimal('100'))
        self.amount_after_tax = self.amount_requested - self.tax_amount
        return self.amount_after_tax
    
    def process_withdrawal(self):
        """Auto-approve and process withdrawal"""
        if self.status == 'completed':
            return False
        
        # Check minimum amount
        if self.amount_requested < self.MINIMUM_WITHDRAWAL:
            self.status = 'failed'
            self.save()
            return False
        
        # Check wallet balance
        if self.wallet.balance < self.amount_requested:
            self.status = 'failed'
            self.save()
            return False
        
        # Calculate taxes
        self.calculate_taxes()
        
        # Debit wallet
        self.wallet.balance -= self.amount_requested
        self.wallet.save()
        
        # Create debit transaction
        Transaction.objects.create(
            wallet=self.wallet,
            amount=self.amount_requested,
            type='debit',
            description=f"Withdrawal via {self.get_payment_method_display()} - {self.amount_after_tax} received (Tax: {self.tax_amount})"
        )
        
        # Mark as completed
        self.status = 'completed'
        self.processed_at = timezone.now()
        self.save()
        
        return True
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Withdrawal Request"
        verbose_name_plural = "Withdrawal Requests"


class AdminTax(models.Model):
    """Track taxes collected from all withdrawals"""
    withdrawal_request = models.OneToOneField(WithdrawalRequest, on_delete=models.CASCADE, related_name='admin_tax')
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)
    collected_from = models.CharField(max_length=255, help_text="Artisan username for reference")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Tax: ${self.tax_amount} from {self.collected_from}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Admin Tax"
        verbose_name_plural = "Admin Taxes"
    
    @classmethod
    def get_total_taxes(cls):
        """Get total taxes collected by admin"""
        from django.db.models import Sum
        result = cls.objects.aggregate(total=Sum('tax_amount'))
        return result['total'] or Decimal('0.00')
