from rest_framework import serializers
from product.models import *


class ProductsSerlizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

