from django.contrib import admin
from .models import CustomerProfile, ArtisanProfile, Wallet, Transaction, WithdrawalRequest, AdminTax


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


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('artisan', 'amount_requested', 'amount_after_tax', 'payment_method', 'status', 'created_at')
    search_fields = ('artisan__username', 'mobile_number', 'bank_account_number')
    readonly_fields = ('created_at', 'processed_at', 'tax_amount', 'amount_after_tax')
    list_filter = ('status', 'payment_method', 'created_at')
    fieldsets = (
        ('Artisan Information', {
            'fields': ('artisan', 'wallet')
        }),
        ('Withdrawal Amount', {
            'fields': ('amount_requested', 'tax_amount', 'amount_after_tax')
        }),
        ('Payment Method', {
            'fields': ('payment_method', 'bank_account_name', 'bank_account_number', 'mobile_number')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'processed_at')
        }),
    )


@admin.register(AdminTax)
class AdminTaxAdmin(admin.ModelAdmin):
    list_display = ('collected_from', 'tax_amount', 'created_at')
    search_fields = ('collected_from',)
    readonly_fields = ('created_at',)
    list_filter = ('created_at',)
    fieldsets = (
        ('Tax Information', {
            'fields': ('tax_amount', 'collected_from')
        }),
        ('Associated Withdrawal', {
            'fields': ('withdrawal_request',)
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
    
    def changelist_view(self, request, extra_context=None):
        """Add total taxes to the admin view"""
        extra_context = extra_context or {}
        from django.db.models import Sum
        total_taxes = AdminTax.objects.aggregate(total=Sum('tax_amount'))['total'] or 0
        extra_context['total_taxes'] = f"${total_taxes:.2f}"
        return super().changelist_view(request, extra_context=extra_context)
