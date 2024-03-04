
from .models import Category
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

class CategorySerializer(serializers.ModelSerializer):
  #children = serializers.ListSerializer(child=RecursiveField(), required=False)
  class Meta:
      model = Category
      fields = '__all__'
