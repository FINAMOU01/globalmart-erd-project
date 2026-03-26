from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display  = ["id", "user", "get_item_count", "get_total", "updated_at"]
    inlines       = [CartItemInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ["id", "customer", "status", "total", "created_at"]
    list_filter   = ["status"]
    inlines       = [OrderItemInline]