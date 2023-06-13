from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem, ShippingAddress
from cart.models import Cart, CartItem
from .serializers import CheckoutSerializer
from rest_framework.permissions import IsAuthenticated


class CheckoutView(APIView):
    """ Api to place the order """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # get the cart for the user
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"message": "No cart found for the user."}, status=status.HTTP_400_BAD_REQUEST)

        # get all cart items associated with the cart
        cart_items = CartItem.objects.filter(cart=cart)

        if cart_items.count() == 0:
            return Response({"message": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # start creating order from the cart
        order = Order(user=cart.user, total_price=cart.total_price)

        # start creating order item from the cart item
        order_items = []
        for item in cart_items:
            order_item = {
                "product": item.product.id,
                "quantity": item.quantity
            }
            if item.quantity > item.product.stock:
                return Response(
                    {"message": f"Insufficient stock for the product {item.product.id}, please update the cart"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            order_items.append(order_item)

        data = {
            "user": order.user.id,
            "total_price": order.total_price,
            "order_items": order_items,
            "shipping_address": {
                "apartment": request.data.get("apartment"),
                "house": request.data.get("house"),
                "street_address": request.data.get("street_address"),
                "city_town": request.data.get("city_town"),
                "zip_postcode": request.data.get("zip_postcode")
            }
        }

        serializer = CheckoutSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            cart_items.delete()  # delete cart items after saving the order
            return Response({"message": "Order placed successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
