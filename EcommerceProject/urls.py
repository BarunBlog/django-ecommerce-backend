from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/user/', include('user.urls')),
    path('api/product/', include('product.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/order/', include('order.urls')),

    path('api-auth/', include('rest_framework.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
