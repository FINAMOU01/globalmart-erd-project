"""
URL routing for database-first API
Exposes raw SQL tables as REST endpoints
"""

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    CustomerTierViewSet, UserViewSet, CategoryViewSet, CurrencyViewSet,
    ProductViewSet, OrderViewSet, OrderItemViewSet, CartItemViewSet, CartViewSet
)

app_name = 'api_raw'

router = SimpleRouter()
router.register(r'customer-tiers', CustomerTierViewSet, basename='customer-tier')
router.register(r'users', UserViewSet, basename='user')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'currencies', CurrencyViewSet, basename='currency')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
router.register(r'cart-items', CartItemViewSet, basename='cart-item')
router.register(r'carts', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]
