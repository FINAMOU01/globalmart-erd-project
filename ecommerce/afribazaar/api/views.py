"""
AfriBazaar REST API Views

Provides ViewSets for all API endpoints using Django REST Framework.
Uses ViewSets + Routers for clean, maintainable code.
Supports full CRUD operations (Create, Read, Update, Delete).
"""

from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q, Count

from products.models import Product, Category, ArtisanRating
from orders.models import Order, OrderItem
from accounts.models import ArtisanProfile

from api.serializers import (
    ProductSerializer,
    ProductListSerializer,
    ArtisanSerializer,
    CategorySerializer,
    OrderSerializer,
    OrderListSerializer,
    ArtisanRatingSerializer,
)

User = get_user_model()


class StandardPagination(PageNumberPagination):
    """Standard pagination for all API views"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product API endpoints.
    
    Supports full CRUD operations:
    - GET /api/products/ -> List all products
    - GET /api/products/<id>/ -> Get product details
    - POST /api/products/ -> Create new product
    - PUT /api/products/<id>/ -> Update entire product
    - PATCH /api/products/<id>/ -> Partial update
    - DELETE /api/products/<id>/ -> Delete product
    
    Custom actions:
    - GET /api/products/featured/ -> Get featured products
    - GET /api/products/by_category/ -> Get products by category
    - GET /api/products/by_artisan/ -> Get products by artisan
    """
    queryset = Product.objects.select_related('artisan', 'category').all()
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'artisan__username']
    ordering_fields = ['created_at', 'price', 'stock_quantity']
    ordering = ['-created_at']
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view"""
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get all featured products.
        
        Usage:
        GET /api/products/featured/
        """
        featured_products = self.queryset.filter(is_featured=True)
        page = self.paginate_queryset(featured_products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Get products by category.
        
        Usage:
        GET /api/products/by_category/?category_id=1
        """
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response(
                {'error': 'category_id query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        products = self.queryset.filter(category_id=category_id)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_artisan(self, request):
        """
        Get products by artisan.
        
        Usage:
        GET /api/products/by_artisan/?artisan_id=1
        """
        artisan_id = request.query_params.get('artisan_id')
        if not artisan_id:
            return Response(
                {'error': 'artisan_id query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        products = self.queryset.filter(artisan_id=artisan_id)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def top_sales(self, request):
        """
        Get top 10 products by sales (most sold products).
        
        Usage:
        GET /api/products/top_sales/
        
        Returns: List of 10 products with the most sales
        """
        # Count how many times each product appears in OrderItem
        top_products = self.queryset.annotate(
            sales_count=Count('orderitem')
        ).order_by('-sales_count')[:10]
        
        serializer = self.get_serializer(top_products, many=True)
        return Response({
            'count': len(top_products),
            'results': serializer.data
        })


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category API endpoints.
    
    Supports full CRUD operations:
    - GET /api/categories/ -> List all categories
    - GET /api/categories/<id>/ -> Get category details
    - POST /api/categories/ -> Create new category
    - PUT /api/categories/<id>/ -> Update entire category
    - PATCH /api/categories/<id>/ -> Partial update
    - DELETE /api/categories/<id>/ -> Delete category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    permission_classes = [permissions.AllowAny]


class ArtisanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Artisan API endpoints.
    
    Supports full CRUD operations:
    - GET /api/artisans/ -> List all artisans
    - GET /api/artisans/<id>/ -> Get artisan details
    - POST /api/artisans/ -> Create new artisan (not recommended - use registration)
    - PUT /api/artisans/<id>/ -> Update entire artisan profile
    - PATCH /api/artisans/<id>/ -> Partial update
    - DELETE /api/artisans/<id>/ -> Delete artisan
    
    Custom actions:
    - GET /api/artisans/<id>/products/ -> Get artisan's products
    - GET /api/artisans/<id>/ratings/ -> Get artisan's ratings
    """
    queryset = User.objects.filter(is_artisan=True).prefetch_related('artisanprofile')
    serializer_class = ArtisanSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username', 'date_joined']
    ordering = ['-date_joined']
    permission_classes = [permissions.AllowAny]
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """
        Get all products by this artisan.
        
        Usage:
        GET /api/artisans/<artisan_id>/products/
        """
        artisan = self.get_object()
        products = Product.objects.filter(artisan=artisan).select_related('category')
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def ratings(self, request, pk=None):
        """
        Get all ratings for this artisan.
        
        Usage:
        GET /api/artisans/<artisan_id>/ratings/
        """
        artisan = self.get_object()
        ratings = ArtisanRating.objects.filter(artisan=artisan)
        page = self.paginate_queryset(ratings)
        if page is not None:
            serializer = ArtisanRatingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ArtisanRatingSerializer(ratings, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Order API endpoints.
    
    Supports full CRUD operations:
    - GET /api/orders/ -> List all orders (paginated)
    - GET /api/orders/<id>/ -> Get order details
    - POST /api/orders/ -> Create new order
    - PUT /api/orders/<id>/ -> Update entire order
    - PATCH /api/orders/<id>/ -> Partial update (e.g., status changes)
    - DELETE /api/orders/<id>/ -> Delete order
    
    Custom actions:
    - GET /api/orders/by_status/?status=pending -> Filter orders by status
    """
    queryset = Order.objects.select_related('customer').prefetch_related('items').all()
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['customer__username', 'customer__email', 'status']
    ordering_fields = ['created_at', 'status', 'total_price']
    ordering = ['-created_at']
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_class(self):
        """Use lightweight serializer for list view"""
        if self.action == 'list':
            return OrderListSerializer
        return OrderSerializer
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """
        Filter orders by status.
        
        Valid statuses: pending, confirmed, processing, shipped, delivered, cancelled
        
        Usage:
        GET /api/orders/by_status/?status=pending
        """
        status_filter = request.query_params.get('status')
        if not status_filter:
            return Response(
                {'error': 'status query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        valid_statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']
        if status_filter not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Valid options: {", ".join(valid_statuses)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        orders = self.queryset.filter(status=status_filter)
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)


class ArtisanRatingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Artisan Rating API endpoints.
    
    Supports full CRUD operations:
    - GET /api/reviews/ -> List all reviews
    - GET /api/reviews/<id>/ -> Get review details
    - POST /api/reviews/ -> Create new review (rating)
    - PUT /api/reviews/<id>/ -> Update entire review
    - PATCH /api/reviews/<id>/ -> Partial update
    - DELETE /api/reviews/<id>/ -> Delete review
    """
    queryset = ArtisanRating.objects.select_related('artisan', 'rater').all()
    serializer_class = ArtisanRatingSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['artisan__username', 'rater__username', 'comment']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']
    permission_classes = [permissions.AllowAny]
