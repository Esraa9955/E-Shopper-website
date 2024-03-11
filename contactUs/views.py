from django.shortcuts import render


from rest_framework import generics
from .models import ContactMessage
from .serializers import ContactMessageSerializer

class ContactMessageListCreateView(generics.ListCreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
