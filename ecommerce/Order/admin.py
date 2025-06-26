from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'total_price', 'order_status', 'created_at', 'updated_at')

    list_filter = ('order_status', 'created_at')

    search_fields = ('user__name', 'product__name', 'order_status')

    ordering = ('-created_at',)

    list_per_page = 20

admin.site.register(Order, OrderAdmin)