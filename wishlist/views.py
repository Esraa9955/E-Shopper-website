from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from wishlist.models import *
from .serlizer import WishlistSerlizer
from rest_framework import status

# Create your views here.
@api_view(['POST'])
def addToList(request):
  user = request.data["user"]
  item = request.data["item"]
  if Wishlist.objects.filter(user=user, item=item).exists():
        return Response({'msg': 'Item already exists in the wishlist'}, status=status.HTTP_400_BAD_REQUEST)
  else:
      wishlist_data = {'user': user, 'item': item}
      serializer = WishlistSerlizer(data=wishlist_data)
      if serializer.is_valid():
          serializer.save()
          return Response({'msg': 'Item added to wishlist'}, status=status.HTTP_201_CREATED)
      else:
          return Response({'msg': 'Invalid data', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteFromList(request,item_id):
  obj = Wishlist.objects.filter(id=item_id).first()
  if obj is not None: 
      obj.delete()
      return Response({'msg': 'deleted'})
  return Response({'msg': 'product not found'})

@api_view(['GET'])
def wishList(request):
  pass