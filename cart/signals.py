from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CartItem


@receiver(post_save, sender=CartItem)
def update_cart_total_price_after_creation(sender, instance, created, **kwargs):
    if created:
        cart = instance.cart
        cart.total_price = cart.calculate_total_price()
        cart.save()


@receiver(post_delete, sender=CartItem)
def update_cart_total_price_after_deletion(sender, instance, **kwargs):
    cart = instance.cart
    cart.total_price = cart.calculate_total_price()
    cart.save()
