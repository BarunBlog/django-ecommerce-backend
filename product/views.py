from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Product, ProductReview
from .serializers import ProductSerializer, ProductReviewSerializer, ProductDetailSerializer
from django.core.exceptions import ValidationError


class GetProducts(generics.ListAPIView):
    """ API to get list of all products with pagination """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailsAPI(APIView):
    """ API to get details of the product with all reviews """

    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            serializer = ProductDetailSerializer(product)

            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=404)


class CreateProductReview(APIView):
    """ API to create product review by the customer """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductReviewSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():

            try:
                serializer.save()  # Save the review to the database
            except ValidationError as e:
                return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
