from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
   path('allproducts/',allProducts,name='allProducts'), 
   path('getProduct/<int:id>/', getproductbyid, name='getproductbyid'),
]
