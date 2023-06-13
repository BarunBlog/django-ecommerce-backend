from .models import Product, ProductReview
from order.models import Order
from rest_framework import serializers
from django.core.exceptions import ValidationError


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "image", "price", "stock"]


class ProductDetailSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "image", "price", "stock", "reviews"]

    def get_reviews(self, obj):
        reviews = ProductReview.objects.filter(product__id=obj.id)
        serializer = ProductReviewSerializer(reviews, many=True)
        return serializer.data


class ProductReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=True)

    class Meta:
        model = ProductReview
        fields = ['product_id', 'rating', 'description', 'verified_purchase']

    def create(self, validated_data):
        validated_data['user'] = self.context['user']

        try:
            product = Product.objects.get(id=validated_data["product_id"])
        except Product.DoesNotExist:
            raise ValidationError("Product not found")

        # Query to check if there exists an order with the given product and user
        order_exists = Order.objects.filter(
            order_items__product_id=product.id,
            user=self.context['user']
        ).exists()

        # Set verified_purchase based on the order_exists condition
        verified_purchase = order_exists

        validated_data['product'] = product
        validated_data['verified_purchase'] = verified_purchase

        return super().create(validated_data)
