from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, ArtisanProfile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin for managing CustomUser with artisan designation.
    """
    list_display = ('username', 'email', 'get_full_name', 'is_artisan', 'is_admin', 'is_active')
    list_filter = ('is_artisan', 'is_admin', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    
    fieldsets = (
        ('Authentication', {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('AfriBazaar Info', {'fields': ('is_artisan', 'is_admin', 'is_active', 'tier_id', 'account_status', 'email_verified', 'email_verified_at')}),
        ('Timestamps', {'fields': ('last_login', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('AfriBazaar Info', {
            'fields': ('is_artisan', 'is_admin', 'tier_id', 'account_status'),
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'


@admin.register(ArtisanProfile)
class ArtisanProfileAdmin(admin.ModelAdmin):
    """
    Admin for managing artisan profiles.
    """
    list_display = ('get_artisan_name', 'get_artisan_username', 'created_at', 'updated_at')
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
    
    def get_artisan_username(self, obj):
        return obj.user.username
    get_artisan_username.short_description = 'Username'
