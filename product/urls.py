from .views import (
    GetProducts,
    CreateProductReview,
    ProductDetailsAPI
)

from django.urls import path


urlpatterns = [
    path('get_products/', GetProducts.as_view(), name="get_products"),
    path('create_product_review/', CreateProductReview.as_view(), name="create_product_review"),
    path('get_product_details/<int:pk>/', ProductDetailsAPI.as_view(), name="get_product_details"),
]

