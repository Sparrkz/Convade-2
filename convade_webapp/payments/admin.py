from django.contrib import admin
from .models import Payment

# Register your models here.


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'created_at']
    search_fields = ['user__username', 'user__email']
    list_filter = ['status', 'created_at']