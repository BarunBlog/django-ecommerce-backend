from rest_framework import serializers
from .models import Cart, CartItem
from django.db.models import F


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)


class GetCartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ["total_price", "created_at", "updated_at", "cart_items"]

    def get_cart_items(self, obj):
        cart_items = CartItem.objects.filter(cart__id=obj.id).annotate(
            productId=F("product__id"),
            product_name=F("product__name"),
            price=F("product__price"),
        ).values("productId", "product_name", "price", "quantity")

        serializer = CartItemSerializer(cart_items, many=True)
        return serializer.data


class CartItemSerializer(serializers.Serializer):

    productId = serializers.IntegerField(required=True)
    product_name = serializers.CharField(max_length=200)
    price = serializers.DecimalField(max_digits=20, decimal_places=2,)
    quantity = serializers.IntegerField(min_value=1, required=True)
