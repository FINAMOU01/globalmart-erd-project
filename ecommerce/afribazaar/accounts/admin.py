from django.contrib import admin
from .models import CustomerProfile, ArtisanProfile


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
    search_fields = ('user__username', 'phone')
    readonly_fields = ('date_joined',)
    list_filter = ('is_verified', 'date_joined')
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
        ('Verification Status', {
            'fields': ('is_verified',)
        }),
        ('Metadata', {
            'fields': ('date_joined',)
        }),
    )
