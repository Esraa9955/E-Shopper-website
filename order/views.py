from rest_framework import viewsets
from .models import Order


class OrderViewSet(viewsets.ModelViewSet):
  serializer_class = Order.objects.all()