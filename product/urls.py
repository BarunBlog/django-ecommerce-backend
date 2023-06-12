from .views import (
    GetProducts,
)

from django.urls import path


urlpatterns = [
    path('get_products/', GetProducts.as_view(), name="get_products"),
]

