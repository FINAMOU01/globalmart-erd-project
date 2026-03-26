from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, ArtisanProfile


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Extended User Admin for managing CustomUser with artisan designation.
    """
    list_display = ('username', 'email', 'get_full_name', 'is_artisan', 'phone', 'country', 'date_joined')
    list_filter = ('is_artisan', 'date_joined', 'country')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('AfriBazaar Info', {'fields': ('is_artisan', 'phone', 'country')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('AfriBazaar Info', {
            'fields': ('is_artisan', 'phone', 'country'),
        }),
    )


@admin.register(ArtisanProfile)
class ArtisanProfileAdmin(admin.ModelAdmin):
    """
    Admin for managing artisan profiles.
    """
    list_display = ('get_artisan_name', 'get_artisan_country', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {'fields': ('user',)}),
        ('Profile Details', {'fields': ('bio', 'profile_image', 'social_links')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    def get_artisan_name(self, obj):
        return obj.user.get_full_name()
    get_artisan_name.short_description = 'Artisan Name'
    
    def get_artisan_country(self, obj):
        return obj.user.country
    get_artisan_country.short_description = 'Country'
