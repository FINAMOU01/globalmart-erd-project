from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """
    Product categories for organizing African cultural products.
    Mapped to schema 'categories' table.
    """
    category_id = models.AutoField(primary_key=True, db_column='category_id')
    name = models.CharField(max_length=200, unique=True, db_column='category_name')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"
        db_table = 'categories'
        managed = False


class Product(models.Model):
    """
    Product model representing African cultural items on the marketplace.
    Mapped to schema 'products' table.
    Images are stored in separate ProductImage table (one-to-many relationship).
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
    
    product_id = models.AutoField(primary_key=True, db_column='product_id')
    artisan = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        limit_choices_to={'is_artisan': True},
        db_column='artisan_id',
        help_text="Only artisans (is_artisan=True) can be product creators"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        db_column='category_id',
        related_name='products'
    )
    name = models.CharField(max_length=255, db_column='product_name')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency_code = models.CharField(
        max_length=3,
        default='USD',
        choices=CURRENCY_CHOICES,
        db_column='currency_code',
        help_text="Currency code"
    )
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    stock_quantity = models.IntegerField(default=0, db_column='stock_quantity')
    reorder_level = models.IntegerField(default=10, db_column='reorder_level')
    is_featured = models.BooleanField(default=False, db_column='is_featured')
    is_active = models.BooleanField(default=True, db_column='is_active')
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, db_column='average_rating')
    review_count = models.IntegerField(default=0, db_column='review_count')
    total_sales = models.IntegerField(default=0, db_column='total_sales')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')
    
    def __str__(self):
        return f"{self.name} - {self.artisan.get_full_name()}"
    
    def get_price_in_currency(self, target_currency_code='USD'):
        """Convert price from product currency to target currency"""
        from payments.models import ExchangeRate
        
        if self.currency_code == target_currency_code:
            return self.price
        
        try:
            # Get latest rates for both currencies
            source_rate = ExchangeRate.objects.filter(currency__currency_code=self.currency_code).latest('date_updated')
            target_rate = ExchangeRate.objects.filter(currency__currency_code=target_currency_code).latest('date_updated')
            
            # Convert: product_price * (source_rate / target_rate)
            converted_price = self.price * (source_rate.rate_to_usd / target_rate.rate_to_usd)
            return round(float(converted_price), 2)
        except Exception as e:
            # Return original price if conversion fails
            return float(self.price)
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'products'
        managed = False
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
    
    rating_id = models.AutoField(primary_key=True, db_column='rating_id')
    artisan = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='artisan_ratings',
        db_column='artisan_id',
        limit_choices_to={'is_artisan': True}
    )
    rater = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='artisan_ratings_given',
        db_column='customer_id'
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, db_column='review_text')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['artisan', 'rater']
        ordering = ['-created_at']
        db_table = 'artisan_ratings'
        managed = False
    
    def __str__(self):
        return f"{self.rater.username} rated {self.artisan.username} - {self.rating}/5"
