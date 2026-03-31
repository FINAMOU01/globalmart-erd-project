from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """
    Product categories for organizing African cultural products.
    """
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"


class Product(models.Model):
    """
    Product model representing African cultural items on the marketplace.
    - artisan: Only users with is_artisan=True can create products
    - attributes: JSONField for flexible product attributes (color, size, material, etc.)
    - currency: The currency the artisan listed the price in
    """
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
    
    artisan = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        limit_choices_to={'is_artisan': True},
        help_text="Only artisans (is_artisan=True) can be product creators"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency_code = models.CharField(
        max_length=3,
        default='USD',
        choices=CURRENCY_CHOICES,
        help_text="Currency code (USD, EUR, XAF, NGN, GHS, KES, ZAR, EGP, MAD, GBP)"
    )
    stock_quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    attributes = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text='JSON format: {"color":"red","size":"M","material":"Ankara"}'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.artisan.get_full_name()}"
    
    def get_price_in_currency(self, target_currency_code='USD'):
        """Convert price from product currency to target currency"""
        from payments.models import ExchangeRate
        
        if self.currency_code == target_currency_code:
            return self.price
        
        try:
            # Get latest rates for both currencies using currency__currency_code
            source_rate = ExchangeRate.objects.filter(currency__currency_code=self.currency_code).latest('date_updated')
            target_rate = ExchangeRate.objects.filter(currency__currency_code=target_currency_code).latest('date_updated')
            
            # Convert: product_price * (source_rate / target_rate)
            # Example: 100 XAF to USD: 100 * (0.00165 / 1.0) = 0.165 USD
            converted_price = self.price * (source_rate.rate_to_usd / target_rate.rate_to_usd)
            return round(float(converted_price), 2)
        except Exception as e:
            # Return original price if conversion fails
            return float(self.price)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['artisan', '-created_at']),
        ]


class ArtisanRating(models.Model):
    """
    Model for rating and reviewing artisans
    """
    RATING_CHOICES = [
        (1, '⭐ Poor'),
        (2, '⭐⭐ Fair'),
        (3, '⭐⭐⭐ Good'),
        (4, '⭐⭐⭐⭐ Very Good'),
        (5, '⭐⭐⭐⭐⭐ Excellent'),
    ]
    
    artisan = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='artisan_ratings',
        limit_choices_to={'is_artisan': True}
    )
    rater = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='artisan_ratings_given'
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['artisan', 'rater']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.rater.username} rated {self.artisan.username} - {self.rating}/5"
