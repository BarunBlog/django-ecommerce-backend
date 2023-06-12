from django.db import models
from django.db.models import Sum, F
from django.contrib.auth.models import User
from product.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Cart'

    def __str__(self):
        return str(self.id)

    def calculate_total_price(self):
        total_price = self.cartitem_set.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total']
        return total_price if total_price is not None else 0


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = (('cart', 'product'),)

    def __str__(self):
        return f"{self.cart} {self.product}"

