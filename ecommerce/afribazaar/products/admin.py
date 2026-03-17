from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin for managing product categories.
    """
    list_display = ('name', 'get_product_count', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Category Information', {'fields': ('name', 'description', 'image')}),
        ('Timestamps', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    
    def get_product_count(self, obj):
        return obj.products.count()
    get_product_count.short_description = 'Total Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin for managing all products.
    """
    list_display = ('name', 'get_artisan_name', 'category', 'price', 'stock_quantity', 'is_featured', 'created_at', 'get_image_preview')
    list_filter = ('category', 'is_featured', 'created_at', 'price')
    search_fields = ('name', 'description', 'artisan__first_name', 'artisan__last_name')
    readonly_fields = ('created_at', 'updated_at', 'get_image_preview')
    
    fieldsets = (
        ('Product Information', {'fields': ('name', 'description', 'category', 'artisan')}),
        ('Pricing & Stock', {'fields': ('price', 'stock_quantity')}),
        ('Media', {'fields': ('image', 'get_image_preview')}),
        ('Product Attributes', {'fields': ('attributes',)}),
        ('Status', {'fields': ('is_featured', 'created_at', 'updated_at')}),
    )
    
    def get_artisan_name(self, obj):
        return obj.artisan.get_full_name()
    get_artisan_name.short_description = 'Artisan'
    
    def get_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="border-radius: 5px;"/>',
                obj.image.url
            )
        return "No Image"
    get_image_preview.short_description = 'Image Preview'
