from .views import (
    AddToCartView,
    GetCartAPI,
    RemoveFromCartView,
)

from django.urls import path


urlpatterns = [
    path('add_to_cart/', AddToCartView.as_view(), name="get_products"),
    path('get_cart/', GetCartAPI.as_view(), name="get_cart"),
    path('remove_from_cart/', RemoveFromCartView.as_view(), name="remove_from_cart"),
]

