from django.contrib import admin
from .models import Cart, CartItem
from rangefilter.filters import DateRangeFilter


class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "total_price", "created_at", "updated_at"]
    list_filter = (
        ('created_at', DateRangeFilter),
        ('updated_at', DateRangeFilter),
    )


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity")


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
