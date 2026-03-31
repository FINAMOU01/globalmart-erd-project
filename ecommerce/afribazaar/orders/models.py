from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class Order(models.Model):
    """
    Order model representing a customer's purchase.
    Tracks all products purchased in a single transaction.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        limit_choices_to={'is_artisan': False}
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer.get_full_name()}"
    
    def get_items_total(self):
        """Calculate total price of all items in this order"""
        return sum(item.get_subtotal() for item in self.items.all())
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer', '-created_at']),
            models.Index(fields=['status']),
        ]


class OrderItem(models.Model):
    """
    Represents individual items within an order.
    Each item links to a product sold by an artisan.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    artisan = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sold_items',
        limit_choices_to={'is_artisan': True}
    )
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    def get_subtotal(self):
        """Calculate subtotal for this order item"""
        return self.price * self.quantity
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['artisan', '-created_at']),
        ]


class Cart(models.Model):
    """
    Shopping cart for storing temporary items before checkout.
    One cart per user at a time.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart - {self.user.get_full_name()}"
    
    @property
    def total_price(self):
        """Calculate total price of all items in cart"""
        return sum(item.subtotal for item in self.items.all())
    
    @property
    def items_count(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())
    
    class Meta:
        ordering = ['-created_at']


class CartItem(models.Model):
    """
    Represents individual items in a shopping cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    @property
    def subtotal(self):
        """Calculate subtotal for this cart item"""
        return self.product.price * self.quantity
    
    class Meta:
        ordering = ['-added_at']
        unique_together = ('cart', 'product')
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['product']),
        ]
