from rest_framework import generics
from .models import Banner
from .serializers import BannerSerializer

class BannerListCreateView(generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer