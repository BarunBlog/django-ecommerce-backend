from django.contrib import admin
from .models import Product, ProductReview


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "price", "stock"]
    search_fields = ("name", )


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "rating", "verified_purchase", "created_at"]
    list_filter = [
        "verified_purchase",
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
