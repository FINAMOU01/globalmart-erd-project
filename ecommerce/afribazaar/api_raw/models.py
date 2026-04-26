"""
Database-First Models for Raw SQL API
Maps directly to existing PostgreSQL tables without migrations
managed = False ensures Django doesn't manage these tables
"""

from django.db import models


class CustomerTier(models.Model):
    """Maps to customer_tiers table"""
    tier_id = models.AutoField(primary_key=True)
    tier_name = models.CharField(max_length=50, unique=True)
    min_annual_spend = models.DecimalField(max_digits=12, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    benefits_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'customer_tiers'
        verbose_name = 'Customer Tier'
        verbose_name_plural = 'Customer Tiers'

    def __str__(self):
        return self.tier_name


class User(models.Model):
    """Maps to users table"""
    ACCOUNT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('deleted', 'Deleted'),
        ('pending_verification', 'Pending Verification'),
    ]

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_artisan = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    account_status = models.CharField(
        max_length=20,
        choices=ACCOUNT_STATUS_CHOICES,
        default='active'
    )
    tier_id = models.IntegerField(default=1)  # FK to customer_tiers
    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.username


class Category(models.Model):
    """Maps to categories table"""
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent_category_id = models.IntegerField(blank=True, null=True)  # Self-reference
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


class Currency(models.Model):
    """Maps to currencies table"""
    currency_code = models.CharField(max_length=3, primary_key=True)
    currency_name = models.CharField(max_length=50)
    currency_symbol = models.CharField(max_length=5)
    is_active = models.BooleanField(default=True)
    decimal_places = models.IntegerField(default=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'currencies'
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return f"{self.currency_code} - {self.currency_name}"


class Product(models.Model):
    """Maps to products table"""
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    artisan_id = models.IntegerField()  # FK to users
    category_id = models.IntegerField()  # FK to categories
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency_code = models.CharField(max_length=3, default='USD')
    sku = models.CharField(max_length=50, blank=True, null=True, unique=True)
    stock_quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.IntegerField(default=0)
    total_sales = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'products'

    def __str__(self):
        return self.product_name


class Order(models.Model):
    """Maps to orders table"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    order_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()  # FK to users
    order_number = models.CharField(max_length=50, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    currency_code = models.CharField(max_length=3, default='USD')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    shipping_address = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    """Maps to order_items table"""
    order_item_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()  # FK to orders
    product_id = models.IntegerField()  # FK to products
    artisan_id = models.IntegerField()  # FK to users
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)  # Generated column in DB
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'order_items'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"Order {self.order_id} - Item {self.order_item_id}"


class CartItem(models.Model):
    """Maps to cart_items table"""
    cart_item_id = models.AutoField(primary_key=True)
    cart_id = models.IntegerField()  # FK to carts
    product_id = models.IntegerField()  # FK to products
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)  # Generated column in DB
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'cart_items'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return f"Cart {self.cart_id} - Item {self.cart_item_id}"


class Cart(models.Model):
    """Maps to carts table"""
    cart_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True)  # FK to users
    total_items = models.IntegerField(default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'carts'

    def __str__(self):
        return f"Cart {self.cart_id}"
