from django.contrib import admin
from .models import Crop, User, Transaction

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'current_price', 'usdc_price', 'last_updated')
    search_fields = ('name', 'code')
    list_filter = ('last_updated',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'name', 'location', 'usdc_balance', 'mpesa_balance', 'rewards_points', 'created_at')
    search_fields = ('phone_number', 'name', 'location')
    list_filter = ('created_at',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'crop', 'quantity', 'total_amount', 'payment_method', 'status', 'tx_hash', 'created_at', 'completed_at')
    search_fields = ('user__phone_number', 'crop__name', 'tx_hash')
    list_filter = ('payment_method', 'status', 'created_at', 'completed_at')
