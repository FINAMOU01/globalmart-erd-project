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
    """
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
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['artisan', '-created_at']),
        ]
