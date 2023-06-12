from .views import (
    UserRegistrationView,
    LogoutAndBlacklistTokenView,
    UserView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path, include


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="create_user"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserView.as_view(), name='profile'),
    path('logout/blacklist/', LogoutAndBlacklistTokenView.as_view(), name='blacklist'),
]

