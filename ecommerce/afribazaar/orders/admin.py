from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username', 'customer__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_item_id', 'order', 'product', 'artisan', 'quantity', 'price')
    list_filter = ('artisan', 'created_at')
    search_fields = ('product__name', 'artisan__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'user', 'items_count', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart_item_id', 'cart', 'product', 'quantity', 'subtotal', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('product__name', 'cart__user__username')
    readonly_fields = ('added_at',)
    ordering = ('-added_at',)
