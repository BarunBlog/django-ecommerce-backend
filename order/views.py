from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem, ShippingAddress
from cart.models import Cart, CartItem
from .serializers import CheckoutSerializer
from rest_framework.permissions import IsAuthenticated
from .stripe import StripeApiHandler
from django.conf import settings


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


class PaymentView(APIView):
    """ Api to create the payment for the customer """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        order_id = request.data.get("order_id")
        payment_method_id = request.data.get("payment_method_id")

        if not order_id:
            return Response({"message": "Please provide the order_id"}, status=status.HTTP_400_BAD_REQUEST)
        if not payment_method_id:
            return Response({"message": "Please provide the payment_method_id"}, status=status.HTTP_400_BAD_REQUEST)

        # get order from the database
        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            return Response({"message": "Invalid order_id"}, status=status.HTTP_400_BAD_REQUEST)

        if order.is_paid:
            return Response({"message": "This order has already been paid"}, status=status.HTTP_400_BAD_REQUEST)

        # instantiating stripe api handler class
        stripe_handler = StripeApiHandler(stripe_secret_key=settings.STRIPE_SECRET_KEY)
        # get or create stripe customer

        try:
            customer_id = stripe_handler.get_or_create_customer(email=user.email, username=user.username)

            # create payment intent for the customer
            payment_intent = stripe_handler.create_payment_intent(
                customer_id=customer_id,
                amount=order.total_price,
                currency='bdt',
                payment_method_id=payment_method_id,
                confirm=True,
                metadata={
                    'order_id': order_id
                }
            )

            order.is_paid = True
            order.save()

            # Creating invoice for the order
            invoice = stripe_handler.create_invoice(
                customer_id=customer_id,
                description=f"Invoice for Order #{order_id}",
                metadata={
                    'customer': user.username,
                    'order_id': order_id,
                    'payment_intent_id': payment_intent.id
                }
            )

            # creating invoice item for each order item
            for order_item in order.order_items.all():
                stripe_handler.create_invoice_item(
                    customer_id=customer_id,
                    invoice_id=invoice.id,
                    amount=(order_item.product.price * order_item.quantity),
                    description=order_item.product.name
                )

            return Response({"message": "Your payment has been completed successfully"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





