from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress
from rangefilter.filters import DateRangeFilter


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "total_price", "order_status", "is_paid", "created_at", "updated_at"]
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
        'order_status',
        'is_paid',
    )


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product", "quantity"]


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "apartment", "house", "street_address", "city_town", "zip_postcode"]
    search_fields = ["apartment", "city_town", "zip+postcode"]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
