from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from order.models import Order
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsDeliveryMan
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes
from order.serializers import OrderSerializer


@api_view(['PUT'])
@permission_classes([IsDeliveryMan])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def updateOrderStatus(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == Order.PENDING_STATE:
        order.status = Order.SHIPPED_STATE
        order.save()
    elif order.status == Order.SHIPPED_STATE:
        order.status = Order.DELIVERED_STATE
        order.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data)
