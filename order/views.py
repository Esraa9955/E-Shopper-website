from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from users.views import *
from product.models import Product   
from .serializers import OrderSerializer
from .models import Order,OrderItem
# Create your views here.


@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders,many=True)
    return Response({'orders':serializer.data})

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def get_order(request,pk):
    order =get_object_or_404(Order, id=pk)

    serializer = OrderSerializer(order,many=False)
    return Response({'order':serializer.data})


@api_view(['PUT'])
#@permission_classes([IsAuthenticated,IsAdminUser])
def process_order(request,pk):
    order =get_object_or_404(Order, id=pk)
    order.status = request.data['status']
    order.save()
     
    serializer = OrderSerializer(order,many=False)
    return Response({'order':serializer.data})


@api_view(['DELETE'])
#@permission_classes([IsAuthenticated])
def delete_order(request,pk):
    order =get_object_or_404(Order, id=pk) 
    order.delete()
      
    return Response({'details': "order is deleted"})




@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def new_order(request):
   
    #print(request.user)
    print(request.data)
    #user= request.user 
    data = request.data
    order_items = data['order_Items']
    print(order_items)

    if order_items and len(order_items) == 0:
        return Response({'error': 'No order received'}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        total_price = sum( item['price']* item['quantity'] for item in order_items)
        order = Order.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            city = data['city'],
            zip_code = data['zip_code'],
            street = data['street'],
            phone_number = data['phone_number'],
            country = data['country'],
            total_price = total_price,
            
            state=data['state'],
        )
        for i in order_items:
            product = Product.objects.get(id=i['product'])
            item = OrderItem.objects.create(
                product= product,
                order = order,
                name = product.name,
                quantity = i['quantity'],
                price = i['price']
            )
            product.stock -= item.quantity
            product.save()
        serializer = OrderSerializer(order,many=False)
        return Response(serializer.data)