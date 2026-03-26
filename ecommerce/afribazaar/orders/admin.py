from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username', 'customer__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'artisan', 'quantity', 'price')
    list_filter = ('artisan', 'created_at')
    search_fields = ('product__name', 'artisan__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
