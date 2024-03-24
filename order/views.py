from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from cart.models import Cart
from users.views import *
from product.models import Product   
from cart.models import Cart   
from .serializers import *
from .models import *
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
from django.http import Http404
from django.db import transaction
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_orders(request):
    orders = Order.objects.order_by('-id')
    serializer = OrderSerializer(orders, many=True)
    return Response({'orders': serializer.data})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_user_orders(request):
    user = request.user
    orders = Order.objects.filter(email=user.email)  # Assuming email is used to identify the user
    serializer = OrderSerializer(orders, many=True)
    return Response({'orders': serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_ordersTmp(request):
    orders = OrderTmp.objects.all() # Fetch all OrderTmp objects
    serializer = OrderTmpSerializer(orders, many=True)  # Serialize queryset
    return Response({'orders': serializer.data})

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#@authentication_classes([TokenAuthentication])
def get_order(request,pk):
    order =get_object_or_404(Order, id=pk)

    serializer = OrderSerializer(order,many=False)
    return Response({'order':serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_orderTmp(request):
    email = request.user.email
    
    try:
        order = OrderTmp.objects.get(email=email)
    except OrderTmp.DoesNotExist:
        raise ValidationError({'error': 'Order not found for this email'})

    serializer = OrderTmpSerializer(order, many=False)
    return Response({'order': serializer.data})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def process_order(request,pk):
    order =get_object_or_404(Order, id=pk)
    order.status = request.data['status']
    order.save()
     
    serializer = OrderSerializer(order,many=False)
    return Response({'order':serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_order(request,pk):
    order =get_object_or_404(Order, id=pk) 
    order.delete()
      
    return Response({'details': "order is deleted"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_orderTmp(request,pk):
    order =get_object_or_404(OrderTmp, id=pk) 
    order.delete()
      
    return Response({'details': "order is deleted"})


@api_view(['POST'])
@transaction.atomic
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def new_orderTmp(request):
    data = request.data
    order_items = data.get('order_Items', [])

    if not order_items or len(order_items) == 0:
        return Response({'error': 'No order received'}, status=status.HTTP_400_BAD_REQUEST)

    zip_code = data.get('zip_code')
    if zip_code is None:
        return Response({'error': 'zip_code is required'}, status=status.HTTP_400_BAD_REQUEST)

    total_price = sum(float(item.get('price', 0)) * int(item.get('quantity', 0)) for item in order_items)
    
    order = OrderTmp.objects.create(
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
        try:
            with transaction.atomic():
                product = Product.objects.get(id=i['product'])
                item = OrderItemTmp.objects.create(
                    product=product,
                    order=order,
                    name=product.name,
                    quantity=i['quantity'],
                    price=i.get('price', 0),  # Use .get() to handle missing 'price' key
                    size=i['size'],  # Use .get() to handle missing 'price' key
                )
                # size=i['size']  # Use .get() to handle missing 'price' key
                # if size == "S":
                #     product.stock_S -= item.quantity
                # elif size == "M":
                #     product.stock_M -= item.quantity
                # elif size == "L":
                #     product.stock_L -= item.quantity
                # elif size == "XL":
                #     product.stock_XL -= item.quantity
                # elif size == "one_size":
                #     product.stock -= item.quantity
                # product.stock -= item.quantity
                product.save()
        except Product.DoesNotExist:
            return Response({'error': f'Product with ID {i["product"]} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    cart_items = Cart.objects.filter()
    # cart_items.delete()
    serializer = OrderTmpSerializer(order, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@transaction.atomic
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

    total_price = sum(float(item.get('price', 0)) * int(item.get('quantity', 0)) for item in order_items)
    
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
        try:
            with transaction.atomic():
                product = Product.objects.get(id=i['product'])
                item = OrderItem.objects.create(
                    product=product,
                    order=order,
                    name=product.name,
                    quantity=i['quantity'],
                    price=i.get('price', 0),  # Use .get() to handle missing 'price' key
                    size = i["size"]
                )
                size=i['size']  # Use .get() to handle missing 'price' key
                if size == "S":
                    product.stock_S -= item.quantity
                elif size == "M":
                    product.stock_M -= item.quantity
                elif size == "L":
                    product.stock_L -= item.quantity
                elif size == "XL":
                    product.stock_XL -= item.quantity
                elif size == "one_size":
                    product.stock -= item.quantity
                # product.stock -= item.quantity
                product.save()
        except Product.DoesNotExist:
            return Response({'error': f'Product with ID {i["product"]} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    cart_items = Cart.objects.filter()
    cart_items.delete()
    serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


'''    for i in order_items:
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
'''



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def cancelOrder(request, pk):
    order = get_object_or_404(Order, id=pk)

    # Check if order status is eligible for cancellation
    if order.status not in [Order.SHIPPED_STATE, Order.DELIVERED_STATE]:
        order.status = Order.CANSCELLED_STATE  # Change status to canceled
        order.save()
        return Response({'msg': 'Order canceled successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'msg': 'Order cannot be canceled, status is already shipped or delivered'}, status=status.HTTP_400_BAD_REQUEST)





#payment
stripe.api_key=settings.STRIPE_SECRET_KEY
success_url = settings.SITE_URL + 'thannk-you/'
API_URL="http/locahost:8000"
class CreateCheckOutSession(APIView):
    def post(self, request, *args, **kwargs):
        # order_id=self.kwargs["pk"]
        total=self.kwargs["pk"]
        try:
            order=OrderTmp.objects.get(id=total)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price_data': {
                            'currency':'usd',
                             'unit_amount':int(order.total_price) * 100,
                             'product_data':{
                                 'name':"total",
                                 #'images':[f"{API_URL}/{orderitem_id.product_image}"]

                             }
                        },
                        'quantity': 1,
                    },
                ],
                # metadata={
                #     "order_id":order.id
                # },
                mode='payment',
                success_url=success_url,  # Updated success_url
                cancel_url=settings.SITE_URL + '?canceled=true',
            )
            return redirect(checkout_session.url)
        except Exception as e:
            return Response({'msg':'something went wrong while creating stripe session','error':str(e)}, status=500)