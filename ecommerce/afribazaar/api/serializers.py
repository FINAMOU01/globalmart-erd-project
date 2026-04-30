"""
AfriBazaar REST API Serializers

Provides ModelSerializers for all main models:
- Product
- Artisan (User + ArtisanProfile)
- Category
- Order
- ArtisanRating
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from products.models import Product, Category, ArtisanRating
from orders.models import Order, OrderItem
from accounts.models import ArtisanProfile

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    Includes basic info about product categories.
    Supports full CRUD operations.
    """
    class Meta:
        model = Category
        fields = ['category_id', 'name', 'description', 'created_at']
        read_only_fields = ['category_id', 'created_at']


class ArtisanProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Artisan Profile.
    Shows artisan details and rating stats.
    """
    average_rating = serializers.SerializerMethodField()
    total_ratings = serializers.SerializerMethodField()
    
    class Meta:
        model = ArtisanProfile
        fields = [
            'id',
            'phone',
            'address',
            'bio',
            'profile_picture',
            'social_links',
            'is_verified',
            'currency_preference',
            'date_joined',
            'average_rating',
            'total_ratings',
        ]
        read_only_fields = ['date_joined', 'average_rating', 'total_ratings']
    
    def get_average_rating(self, obj):
        """Calculate average rating for this artisan"""
        return obj.get_average_rating()
    
    def get_total_ratings(self, obj):
        """Get total number of ratings"""
        return obj.get_total_ratings()


class ArtisanSerializer(serializers.ModelSerializer):
    """
    Serializer for Artisan user with profile information.
    Combines User and ArtisanProfile data.
    """
    profile = ArtisanProfileSerializer(source='artisanprofile', read_only=True)
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_artisan',
            'profile',
            'products_count',
        ]
        read_only_fields = ['user_id', 'is_artisan']
    
    def get_products_count(self, obj):
        """Get number of products by this artisan"""
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    Includes nested category and artisan information.
    Supports full CRUD operations.
    """
    category_id = serializers.IntegerField(write_only=True, required=False)
    artisan_id = serializers.IntegerField(write_only=True, required=False)
    category = CategorySerializer(read_only=True)
    artisan = ArtisanSerializer(read_only=True)
    formatted_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'product_id',
            'artisan',
            'artisan_id',
            'category',
            'category_id',
            'name',
            'description',
            'price',
            'currency_code',
            'formatted_price',
            'stock_quantity',
            'sku',
            'reorder_level',
            'is_featured',
            'is_active',
            'average_rating',
            'review_count',
            'total_sales',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['product_id', 'created_at', 'updated_at']
    
    def get_formatted_price(self, obj):
        """Return price formatted with currency symbol"""
        return f"{obj.price} {obj.currency_code}"
    
    def create(self, validated_data):
        """Create new product with artisan_id and category_id"""
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Update product with artisan_id and category_id"""
        return super().update(instance, validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for product lists.
    Used for list views to reduce payload.
    """
    artisan_name = serializers.CharField(source='artisan.get_full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    formatted_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'product_id',
            'name',
            'artisan_name',
            'category_name',
            'price',
            'currency_code',
            'formatted_price',
            'stock_quantity',
            'is_featured',
            'created_at',
        ]
        read_only_fields = ['product_id', 'created_at']
    
    def get_formatted_price(self, obj):
        """Return price formatted with currency symbol"""
        return f"{obj.price} {obj.currency_code}"


class ArtisanRatingSerializer(serializers.ModelSerializer):
    """
    Serializer for Artisan ratings and reviews.
    Shows rating, comment, and rater information.
    Supports full CRUD operations.
    """
    artisan_id = serializers.IntegerField(write_only=True, required=False)
    rater_id = serializers.IntegerField(write_only=True, required=False)
    rater_username = serializers.CharField(source='rater.username', read_only=True)
    rater_name = serializers.CharField(source='rater.get_full_name', read_only=True)
    artisan_name = serializers.CharField(source='artisan.get_full_name', read_only=True)
    rating_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ArtisanRating
        fields = [
            'rating_id',
            'artisan_id',
            'artisan_name',
            'rater_id',
            'rater_username',
            'rater_name',
            'rating',
            'rating_display',
            'comment',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['rating_id', 'created_at', 'updated_at']
    
    def get_rating_display(self, obj):
        """Get the display label for rating"""
        rating_choices = {
            1: '⭐ Poor',
            2: '⭐⭐ Fair',
            3: '⭐⭐⭐ Good',
            4: '⭐⭐⭐⭐ Very Good',
            5: '⭐⭐⭐⭐⭐ Excellent',
        }
        return rating_choices.get(obj.rating, f'{obj.rating}/5')


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for individual items within an order.
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    artisan_name = serializers.CharField(source='artisan.get_full_name', read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = [
            'order_item_id',
            'product_name',
            'artisan_name',
            'quantity',
            'price',
            'subtotal',
            'created_at',
        ]
        read_only_fields = ['order_item_id', 'created_at']
    
    def get_subtotal(self, obj):
        """Calculate subtotal for this order item"""
        return float(obj.get_subtotal())


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    Includes nested order items and customer information.
    Supports full CRUD operations.
    """
    customer_id = serializers.IntegerField(write_only=True, required=False)
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    customer_email = serializers.CharField(source='customer.email', read_only=True)
    items_count = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'order_id',
            'customer_id',
            'customer_name',
            'customer_email',
            'status',
            'total_price',
            'items_count',
            'total_items',
            'items',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['order_id', 'total_price', 'created_at', 'updated_at']
    
    def get_items_count(self, obj):
        """Get number of different items in this order"""
        return obj.items.count()
    
    def get_total_items(self, obj):
        """Get total quantity of items in this order"""
        return sum(item.quantity for item in obj.items.all())


class OrderListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for order lists.
    Used for list views to reduce payload.
    """
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'order_id',
            'customer_name',
            'status',
            'total_price',
            'items_count',
            'created_at',
        ]
        read_only_fields = ['order_id', 'created_at']
    
    def get_items_count(self, obj):
        """Get number of items in this order"""
        return obj.items.count()
