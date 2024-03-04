
from .models import Category, SubCategory
from rest_framework import serializers

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
  children = SubCategorySerializer(many=True, read_only=True)
  class Meta:
      model = Category
      fields = '__all__'
