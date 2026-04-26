"""Serializers for database-first API with full CRUD support
Flat JSON structure - maps directly to database fields
Supports: GET, POST, PUT, PATCH, DELETE
"""

from rest_framework import serializers
from .models import (
    CustomerTier, User, Category, Currency, Product, Order, OrderItem, CartItem, Cart
)


class CustomerTierSerializer(serializers.ModelSerializer):
    """Full CRUD serializer for customer_tiers table"""

    class Meta:
        model = CustomerTier
        fields = [
            'tier_id', 'tier_name', 'min_annual_spend',
            'discount_percentage', 'benefits_description',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['tier_id', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Full CRUD serializer for users table"""

    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email', 'password_hash',
            'first_name', 'last_name', 'phone_number',
            'is_artisan', 'is_admin', 'is_active',
            'account_status', 'tier_id', 'email_verified',
            'email_verified_at', 'last_login', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user_id', 'email_verified_at', 'last_login', 'created_at', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    """Full CRUD serializer for categories table"""

    class Meta:
        model = Category
        fields = [
            'category_id', 'category_name', 'description',
            'parent_category_id', 'is_active', 'display_order',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['category_id', 'created_at', 'updated_at']


class CurrencySerializer(serializers.ModelSerializer):
    """Full CRUD serializer for currencies table"""

    class Meta:
        model = Currency
        fields = [
            'currency_code', 'currency_name', 'currency_symbol',
            'is_active', 'decimal_places', 'created_at'
        ]
        read_only_fields = ['currency_code', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    """Full CRUD serializer for products table"""

    class Meta:
        model = Product
        fields = [
            'product_id', 'product_name', 'description',
            'artisan_id', 'category_id', 'price', 'currency_code',
            'sku', 'stock_quantity', 'reorder_level',
            'is_featured', 'is_active', 'average_rating',
            'review_count', 'total_sales', 'created_at', 'updated_at'
        ]
        read_only_fields = ['product_id', 'average_rating', 'review_count', 'total_sales', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    """Full CRUD serializer for orders table"""

    class Meta:
        model = Order
        fields = [
            'order_id', 'customer_id', 'order_number', 'order_date',
            'status', 'currency_code', 'subtotal', 'tax_amount',
            'shipping_cost', 'discount_amount', 'total_amount',
            'payment_method', 'payment_status', 'shipping_address',
            'billing_address', 'notes', 'created_at', 'updated_at',
            'shipped_at', 'delivered_at'
        ]
        read_only_fields = ['order_id', 'order_number', 'total_amount', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    """Full CRUD serializer for order_items table"""

    class Meta:
        model = OrderItem
        fields = [
            'order_item_id', 'order_id', 'product_id', 'artisan_id',
            'quantity', 'unit_price', 'subtotal', 'created_at'
        ]
        read_only_fields = ['order_item_id', 'subtotal', 'created_at']


class CartItemSerializer(serializers.ModelSerializer):
    """Full CRUD serializer for cart_items table"""

    class Meta:
        model = CartItem
        fields = [
            'cart_item_id', 'cart_id', 'product_id',
            'quantity', 'unit_price', 'subtotal', 'added_at'
        ]
        read_only_fields = ['cart_item_id', 'subtotal', 'added_at']


class CartSerializer(serializers.ModelSerializer):
    """Full CRUD serializer for carts table"""

    class Meta:
        model = Cart
        fields = [
            'cart_id', 'user_id', 'total_items', 'subtotal',
            'created_at', 'updated_at', 'expires_at'
        ]
        read_only_fields = ['cart_id', 'total_items', 'subtotal', 'created_at', 'updated_at']
