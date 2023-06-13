from django.contrib import admin
from .models import StripeCustomer


class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "stripe_customer_id"]


admin.site.register(StripeCustomer, StripeCustomerAdmin)
