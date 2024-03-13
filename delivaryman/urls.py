
from django.urls import path
from .views import *
from order import views
from order.views import *
# from .views import  CreateCheckOutSession 


urlpatterns = [
    path('update/<int:order_id>', updateOrderStatus),
]