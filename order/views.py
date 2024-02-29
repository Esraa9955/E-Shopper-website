from rest_framework import viewsets
from .models import Order
from rest_framework.permissions import IsAuthenticated
from .selializers import OrderSerializer, CreateOrderSerializer
class OrderViewSet(viewsets.ModelViewSet):
  permission_classes = [IsAuthenticated]
  
  #queryset = Order.objects.all()
  def get_serializer_class(self):
    if self.request.method == 'POST':
      return CreateOrderSerializer
    return OrderSerializer

   
  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return Order.objects.all()
    return Order.objects.filter(buyer=user)
  
  def get_serializer_context(self):
    return {"user_id":self.request.user.id}
  
