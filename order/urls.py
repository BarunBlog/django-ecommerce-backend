from .views import (
    CheckoutView,
    PaymentView
)

from django.urls import path


urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('payment/', PaymentView.as_view(), name="payment"),
]

