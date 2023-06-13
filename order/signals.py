from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem


@receiver(post_save, sender=OrderItem)
def update_product_stock(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        quantity = instance.quantity
        product.stock -= quantity
        product.save()
