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
    path('API/',include('contactUs.urls')),
    path('api/', include('users.urls')),
    path('api/', include('plan.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/wishlist/', include('wishlist.urls')),
    path('API/Review/',include('review.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('verify-email/', verify_email, name='verify_email'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)