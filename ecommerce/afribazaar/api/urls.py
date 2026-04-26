"""
AfriBazaar REST API URL Configuration

This module defines all REST API endpoints using Django REST Framework Routers.
All endpoints are prefixed with /api/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    ProductViewSet,
    ArtisanViewSet,
    CategoryViewSet,
    OrderViewSet,
    ArtisanRatingViewSet,
)

# Create router and register all viewsets
router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='product')
router.register(r'artisans', ArtisanViewSet, basename='artisan')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reviews', ArtisanRatingViewSet, basename='review')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]

"""
AVAILABLE ENDPOINTS:

=== PRODUCTS ===
GET    /api/products/                      List all products (with pagination)
GET    /api/products/<id>/                 Get product details
GET    /api/products/featured/             Get all featured products
GET    /api/products/by_category/?category_id=1    Get products by category
GET    /api/products/by_artisan/?artisan_id=1      Get products by artisan

Query Parameters:
- search=<query>     Search in product name, description, artisan username
- ordering=-created_at   Order by field (use - for descending)
- page_size=50       Customize page size (default 20)
- page=2             Get specific page

=== ARTISANS ===
GET    /api/artisans/                      List all artisans (with pagination)
GET    /api/artisans/<id>/                 Get artisan details
GET    /api/artisans/<id>/products/        Get artisan's products
GET    /api/artisans/<id>/ratings/         Get artisan's ratings

Query Parameters:
- search=<query>     Search in username, first_name, last_name, email
- ordering=username  Order by field
- page_size=50       Customize page size

=== CATEGORIES ===
GET    /api/categories/                    List all categories
GET    /api/categories/<id>/               Get category details

Query Parameters:
- search=<query>     Search in category name and description
- ordering=name      Order by field

=== ORDERS ===
GET    /api/orders/                        List all orders (with pagination)
GET    /api/orders/<id>/                   Get order details (includes order items)
GET    /api/orders/by_status/?status=pending   Filter orders by status

Valid status values: pending, confirmed, processing, shipped, delivered, cancelled

Query Parameters:
- search=<query>     Search in customer username, email, status
- ordering=-created_at   Order by field
- page_size=50       Customize page size

=== REVIEWS (Artisan Ratings) ===
GET    /api/reviews/                       List all reviews (with pagination)
GET    /api/reviews/<id>/                  Get review details

Query Parameters:
- search=<query>     Search in artisan username, rater username, comment text
- ordering=-rating   Order by field
- page_size=50       Customize page size

=== PAGINATION EXAMPLE ===
GET    /api/products/?page=1&page_size=50

Returns:
{
    "count": 234,
    "next": "http://api.example.com/api/products/?page=2",
    "previous": null,
    "results": [...]
}
"""
