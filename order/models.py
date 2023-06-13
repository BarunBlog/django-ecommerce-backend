from django.db import models
from django.contrib.auth.models import User
from product.models import Product

ORDER_STATUS_CHOICES = (
    ('pending', 'pending'),
    ('confirmed', 'confirmed'),
    ('delivered', 'delivered'),
    ('canceled', 'canceled'),
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default="pending")
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Order'

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = (('order', 'product'),)

    def __str__(self):
        return f"{self.order} {self.product}"


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    apartment = models.CharField(max_length=100)
    house = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    city_town = models.CharField(max_length=100)
    zip_postcode = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.apartment}"

