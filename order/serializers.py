from rest_framework import serializers
from .models import Order, OrderItem, ShippingAddress
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['apartment', 'house', 'street_address', 'city_town', 'zip_postcode']


class CheckoutSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    shipping_address = ShippingAddressSerializer()

    class Meta:
        model = Order
        fields = ['user', 'total_price', 'order_items', 'shipping_address']

    def create(self, validated_data):

        # starting database transaction
        with transaction.atomic():
            order_items = validated_data.pop('order_items')
            shipping_address = validated_data.pop('shipping_address')

            # creating order object
            order = Order.objects.create(**validated_data)

            # creating order_items
            for item in order_items:
                try:
                    OrderItem.objects.create(order=order, **item)
                except IntegrityError as e:
                    raise ValidationError({"Product": "Duplicate product found"})

            # creating shipping address
            ShippingAddress.objects.create(order=order, **shipping_address)

            return order
