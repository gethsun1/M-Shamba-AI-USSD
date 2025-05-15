from django.contrib import admin
from .models import Crop, User, Transaction

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_sw', 'code', 'current_price', 'last_updated')
    search_fields = ('name', 'code')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'name', 'location', 'mpesa_balance', 'usdc_balance', 'rewards_points')
    search_fields = ('phone_number', 'name')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'crop', 'quantity', 'price_per_kg', 'total_amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__phone_number', 'crop__name')
