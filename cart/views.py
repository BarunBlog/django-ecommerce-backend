from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cart, CartItem
from product.models import Product
from rest_framework.permissions import IsAuthenticated
from .serializers import AddToCartSerializer, GetCartSerializer
from django.db import IntegrityError


class AddToCartView(APIView):
    """ Api to add the product to cart """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():

            product_id = request.data["product_id"]
            quantity = request.data["quantity"]

            # get product from product_id
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"message": "invalid product_id"}, status=status.HTTP_400_BAD_REQUEST)

            # check if we have enough products in stock
            if int(quantity) > product.stock:
                return Response({"message": f"Insufficient stock for the product {product.id}"},
                                status=status.HTTP_400_BAD_REQUEST)

            # check if the user has a cart, if not then create a new one
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Create the cart item to add product to cart item
            try:
                CartItem.objects.create(cart=cart, product=product, quantity=quantity)
            except IntegrityError as e:
                print(e, flush=True)
                return Response({"error": "Product already exists"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Product added to the cart"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCartAPI(APIView):
    """ Api to list all products in a cart """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.get(user__id=request.user.id)
        except Cart.DoesNotExist:
            return Response({"message": "You don't have any cart yet"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GetCartSerializer(cart)
        return Response(serializer.data)


class RemoveFromCartView(APIView):
    """ Api to remove the product from the cart """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"message": "Please provide the product_id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return Response({"message": "Product removed from the cart successfully."})
        except Cart.DoesNotExist:
            return Response({"message": "Cart does not exist for the user."}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"message": "Product does not exist in the cart."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "An error occurred while removing the product from the cart."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


