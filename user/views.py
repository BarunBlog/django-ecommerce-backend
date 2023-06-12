from django.http import Http404
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import (
    UserCreateSerializer,
    UserSerializer,
)
from django.contrib.auth.models import User


class UserRegistrationView(generics.CreateAPIView):
    """ Api to register the user """
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User registration successful"},
            status=status.HTTP_201_CREATED
        )


class UserView(APIView):
    """
    Retrieve, update or delete a user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class LogoutAndBlacklistTokenView(APIView):
    """ Api to log out the user """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if "refresh_token" not in request.data:
            return Response({"message": "Please provide refresh_token in the body"})
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "User logged out successfully."})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
