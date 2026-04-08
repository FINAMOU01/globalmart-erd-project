from django.contrib import admin
from .models import CustomerProfile, ArtisanProfile, Wallet, Transaction


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'date_joined')
    search_fields = ('user__username', 'phone')
    readonly_fields = ('date_joined',)
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'address')
        }),
        ('Profile Picture', {
            'fields': ('profile_picture',)
        }),
        ('Metadata', {
            'fields': ('date_joined',)
        }),
    )


@admin.register(ArtisanProfile)
class ArtisanProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_verified', 'date_joined')
    search_fields = ('user__username', 'phone', 'bio')
    readonly_fields = ('date_joined',)
    list_filter = ('is_verified', 'date_joined')
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Biography', {
            'fields': ('bio',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'address')
        }),
        ('Profile Picture', {
            'fields': ('profile_picture',)
        }),
        ('Verification Status', {
            'fields': ('is_verified',)
        }),
        ('Metadata', {
            'fields': ('date_joined',)
        }),
    )


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('artisan', 'balance', 'created_at', 'updated_at')
    search_fields = ('artisan__username',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Artisan Information', {
            'fields': ('artisan',)
        }),
        ('Balance', {
            'fields': ('balance',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('get_artisan', 'type', 'amount', 'description', 'created_at')
    search_fields = ('wallet__artisan__username', 'description')
    readonly_fields = ('created_at',)
    list_filter = ('type', 'created_at')
    fieldsets = (
        ('Wallet Information', {
            'fields': ('wallet',)
        }),
        ('Transaction Details', {
            'fields': ('type', 'amount', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
    
    def get_artisan(self, obj):
        return obj.wallet.artisan.username
    get_artisan.short_description = 'Artisan'
