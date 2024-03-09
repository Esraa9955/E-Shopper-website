from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from cart.models import Cart
from users.views import *
from product.models import Product   
from .serializers import OrderSerializer
from .models import Order,OrderItem
# checkout 
from rest_framework import response
from django.http import HttpResponse
import stripe
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions
#from payment.serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
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
@permission_classes([IsAuthenticated])
def delete_order(request,pk):
    order =get_object_or_404(Order, id=pk) 
    order.delete()
      
    return Response({'details': "order is deleted"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def new_order(request):
    data = request.data
    order_items = data.get('order_Items', [])

    if not order_items or len(order_items) == 0:
        return Response({'error': 'No order received'}, status=status.HTTP_400_BAD_REQUEST)

    zip_code = data.get('zip_code')
    if zip_code is None:
        return Response({'error': 'zip_code is required'}, status=status.HTTP_400_BAD_REQUEST)

    total_price = sum(float(item['price']) * int(item['quantity']) for item in order_items)
    order = Order.objects.create(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        city=data['city'],
        zip_code=zip_code,
        street=data['street'],
        phone_number=data['phone_number'],
        country=data['country'],
        total_price=total_price,
        state=data['state'],
    )

    for i in order_items:
        product = Product.objects.get(id=i['product'])
        item = OrderItem.objects.create(
            product=product,
            order=order,
            name=product.name,
            quantity=i['quantity'],
            price=i['price']
        )
        product.stock -= item.quantity
        product.save()
    
    cart_items = Cart.objects.filter()
    cart_items.delete()
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


#payment
stripe.api_key=settings.STRIPE_SECRET_KEY

API_URL="http/locahost:8000"
class CreateCheckOutSession(APIView):
    def post(self, request, *args, **kwargs):
        orderitem_id=self.kwargs["pk"]
        try:
            order_item=OrderItem.objects.get(id=orderitem_id)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price_data': {
                            'currency':'usd',
                             'unit_amount':int(orderitem_id.price) * 100,
                             'product_data':{
                                 'name':orderitem_id.name,
                                 'images':[f"{API_URL}/{orderitem_id.product_image}"]

                             }
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    "product_id":orderitem_id.id
                },
                mode='payment',
                success_url=settings.SITE_URL + '?success=true',
                cancel_url=settings.SITE_URL + '?canceled=true',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return Response({'msg':'something went wrong while creating stripe session','error':str(e)}, status=500)