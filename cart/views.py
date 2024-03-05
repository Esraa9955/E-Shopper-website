from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from cart.models import *
from .serlizer import CartSerlizer
from rest_framework import status


@api_view(['POST'])
def addToCart(request):
    serializer = CartSerlizer(data=request.data)
    if serializer.is_valid():
        user = request.user
        item = serializer.validated_data['item']

        # Check if the user has already added the same item to the cart
        existing_cart_item = Cart.objects.filter(user=user, item=item).first()
        if existing_cart_item:
            # If the item already exists in the cart, increase the quantity if less than stock
            quantity_to_add = serializer.validated_data['quantity']
            if existing_cart_item.quantity + quantity_to_add > item.stock:
                return Response({'msg': 'Quantity exceeds stock limit'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                existing_cart_item.quantity += quantity_to_add
                existing_cart_item.save()
                total_item_price = existing_cart_item.get_total_item_price()
                return Response({'msg': 'Quantity increased in cart', 'total_item_price': total_item_price}, status=status.HTTP_200_OK)
        else:
            # If the item does not exist in the cart, create a new cart item
            serializer.save(user=user)
            cart = serializer.instance
            total_item_price = cart.get_total_item_price()
            return Response({'msg': 'Item added to cart', 'total_item_price': total_item_price}, status=status.HTTP_201_CREATED)
    else:
        errors = serializer.errors
        return Response({'msg': 'Invalid data', 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
  

@api_view(['DELETE'])
def deleteFromCart(request, cart_id):
    obj = Cart.objects.filter(id=cart_id).first()
    if obj is not None: 
        obj.delete()
        return Response({'msg': 'deleted'})
    return Response({'msg': 'product not found'})

@api_view(['PUT'])
def reduceCartItemQuantity(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)

    if request.method == 'PUT':
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
            total_item_price = cart.get_total_item_price()
            return Response({'msg': 'Quantity reduced successfully','total_item_price': total_item_price})
        else:
            return Response({'msg': 'Quantity cannot be reduced further'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'msg': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT'])
def increaseCartItemQuantity(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)

    if request.method == 'PUT':
        if cart.item.stock > cart.quantity:  # Check if increasing quantity exceeds stock limit
            cart.quantity += 1
            cart.save()

            # Recalculate total item price
            total_item_price = cart.get_total_item_price()

            return Response({'msg': 'Quantity increased successfully', 'total_item_price': total_item_price})
        else:
            return Response({'msg': 'Quantity cannot be increased further, exceeds stock limit'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'msg': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def listCartItems(request, user_id):
    user_carts = Cart.objects.filter(user_id=user_id)
    serializer = CartSerlizer(user_carts, many=True)
    total_items_price = 0
    for cart_item in user_carts:
        total_items_price += cart_item.get_total_item_price()
    response_data = {
        'cart_items': serializer.data,
        'total_items_price': total_items_price
    }
    
    return Response(response_data)
