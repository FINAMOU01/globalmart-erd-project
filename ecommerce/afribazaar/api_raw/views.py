"""Full CRUD ViewSets for database-first API
No business logic - direct database access
SUPPORTS: GET, POST, PUT, PATCH, DELETE
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import permissions

from .models import (
    CustomerTier, User, Category, Currency, Product, Order, OrderItem, CartItem, Cart
)
from .serializers import (
    CustomerTierSerializer, UserSerializer, CategorySerializer, CurrencySerializer,
    ProductSerializer, OrderSerializer, OrderItemSerializer, CartItemSerializer, CartSerializer
)


class StandardPagination(PageNumberPagination):
    """Standard pagination for all endpoints"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomerTierViewSet(ModelViewSet):
    """Full CRUD API endpoint for customer_tiers table
    
    GET /api/raw/customer-tiers/ - List all
    POST /api/raw/customer-tiers/ - Create new
    GET /api/raw/customer-tiers/<id>/ - Retrieve
    PUT /api/raw/customer-tiers/<id>/ - Full update
    PATCH /api/raw/customer-tiers/<id>/ - Partial update
    DELETE /api/raw/customer-tiers/<id>/ - Delete
    """
    queryset = CustomerTier.objects.all()
    serializer_class = CustomerTierSerializer
    pagination_class = StandardPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['tier_name']
    ordering_fields = ['tier_id', 'tier_name', 'min_annual_spend', 'discount_percentage']
    ordering = ['tier_id']
    permission_classes = [permissions.AllowAny]


class UserViewSet(ModelViewSet):
    """Full CRUD API endpoint for users table
    
    GET /api/raw/users/ - List all
    POST /api/raw/users/ - Create new
    GET /api/raw/users/<id>/ - Retrieve
    PUT /api/raw/users/<id>/ - Full update
    PATCH /api/raw/users/<id>/ - Partial update
    DELETE /api/raw/users/<id>/ - Delete
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['user_id', 'username', 'email', 'is_artisan', 'is_admin', 'account_status', 'created_at']
    ordering = ['user_id']
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(ModelViewSet):
    """Full CRUD API endpoint for categories table
    
    GET /api/raw/categories/ - List all
    POST /api/raw/categories/ - Create new
    GET /api/raw/categories/<id>/ - Retrieve
    PUT /api/raw/categories/<id>/ - Full update
    PATCH /api/raw/categories/<id>/ - Partial update
    DELETE /api/raw/categories/<id>/ - Delete
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['category_name', 'description']
    ordering_fields = ['category_id', 'category_name', 'is_active', 'display_order', 'created_at']
    ordering = ['display_order', 'category_id']
    permission_classes = [permissions.AllowAny]


class CurrencyViewSet(ModelViewSet):
    """Full CRUD API endpoint for currencies table
    
    GET /api/raw/currencies/ - List all
    POST /api/raw/currencies/ - Create new
    GET /api/raw/currencies/<id>/ - Retrieve
    PUT /api/raw/currencies/<id>/ - Full update
    PATCH /api/raw/currencies/<id>/ - Partial update
    DELETE /api/raw/currencies/<id>/ - Delete
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = StandardPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['currency_code', 'currency_name']
    ordering_fields = ['currency_code', 'currency_name', 'is_active', 'decimal_places']
    ordering = ['currency_code']
    permission_classes = [permissions.AllowAny]


class ProductViewSet(ModelViewSet):
    """Full CRUD API endpoint for products table
    
    GET /api/raw/products/ - List all
    POST /api/raw/products/ - Create new
    GET /api/raw/products/<id>/ - Retrieve
    PUT /api/raw/products/<id>/ - Full update
    PATCH /api/raw/products/<id>/ - Partial update
    DELETE /api/raw/products/<id>/ - Delete
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['product_name', 'description', 'sku']
    ordering_fields = [
        'product_id', 'product_name', 'price', 'stock_quantity',
        'average_rating', 'review_count', 'total_sales', 'is_featured',
        'is_active', 'created_at', 'artisan_id', 'category_id'
    ]
    ordering = ['product_id']
    permission_classes = [permissions.AllowAny]


class OrderViewSet(ModelViewSet):
    """Full CRUD API endpoint for orders table
    
    GET /api/raw/orders/ - List all
    POST /api/raw/orders/ - Create new
    GET /api/raw/orders/<id>/ - Retrieve
    PUT /api/raw/orders/<id>/ - Full update
    PATCH /api/raw/orders/<id>/ - Partial update
    DELETE /api/raw/orders/<id>/ - Delete
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = StandardPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['order_number']
    ordering_fields = [
        'order_id', 'order_number', 'order_date', 'status',
        'total_amount', 'payment_status', 'customer_id', 'created_at'
    ]
    ordering = ['-order_date']
    permission_classes = [permissions.AllowAny]


class OrderItemViewSet(ModelViewSet):
    """Full CRUD API endpoint for order_items table
    
    GET /api/raw/order-items/ - List all
    POST /api/raw/order-items/ - Create new
    GET /api/raw/order-items/<id>/ - Retrieve
    PUT /api/raw/order-items/<id>/ - Full update
    PATCH /api/raw/order-items/<id>/ - Partial update
    DELETE /api/raw/order-items/<id>/ - Delete
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter]
    ordering_fields = [
        'order_item_id', 'order_id', 'product_id', 'artisan_id',
        'quantity', 'unit_price', 'subtotal', 'created_at'
    ]
    ordering = ['order_item_id']
    permission_classes = [permissions.AllowAny]


class CartItemViewSet(ModelViewSet):
    """Full CRUD API endpoint for cart_items table
    
    GET /api/raw/cart-items/ - List all
    POST /api/raw/cart-items/ - Create new
    GET /api/raw/cart-items/<id>/ - Retrieve
    PUT /api/raw/cart-items/<id>/ - Full update
    PATCH /api/raw/cart-items/<id>/ - Partial update
    DELETE /api/raw/cart-items/<id>/ - Delete
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter]
    ordering_fields = [
        'cart_item_id', 'cart_id', 'product_id',
        'quantity', 'unit_price', 'subtotal', 'added_at'
    ]
    ordering = ['cart_id', 'cart_item_id']
    permission_classes = [permissions.AllowAny]


class CartViewSet(ModelViewSet):
    """Full CRUD API endpoint for carts table
    
    GET /api/raw/carts/ - List all
    POST /api/raw/carts/ - Create new
    GET /api/raw/carts/<id>/ - Retrieve
    PUT /api/raw/carts/<id>/ - Full update
    PATCH /api/raw/carts/<id>/ - Partial update
    DELETE /api/raw/carts/<id>/ - Delete
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    pagination_class = StandardPagination
    filter_backends = [OrderingFilter]
    ordering_fields = [
        'cart_id', 'user_id', 'total_items', 'subtotal',
        'created_at', 'updated_at', 'expires_at'
    ]
    ordering = ['cart_id']
    permission_classes = [permissions.AllowAny]
