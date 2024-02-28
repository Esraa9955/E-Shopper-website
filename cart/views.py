from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from cart.models import *
from .serlizer import CartSerlizer


@api_view(['POST'])
def addToCart(request):
  serializer = CartSerlizer(data=request.data)
  if serializer.is_valid():
      serializer.save()
      return Response({'msg': 'added'})
  else:
      print(serializer.errors)
      return Response({'msg': 'wrong data', 'error': serializer.errors})
