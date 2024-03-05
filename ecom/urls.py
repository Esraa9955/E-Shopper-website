from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from users.views import *


urlpatterns = [

    path('admin/', admin.site.urls),
    path('API/',include('product.urls')),
    path('API/',include('category.urls')),
    path('API/',include('order.urls')),
    path('api/', include('users.urls')),
    path('api/cart/', include('cart.urls')),
    path('API/Review/',include('review.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('verify-email/', verify_email, name='verify_email')

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)