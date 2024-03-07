
from .models import Category, SubCategory
from rest_framework import serializers

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

  class Meta:
      model = Category
      fields = '__all__'
  subcategories= serializers.SerializerMethodField(method_name="get_subcategories", read_only=True)
  def get_subcategories(self,obj):
        subcategory = obj.chiled.all()
        serializer = SubCategorySerializer(subcategory,many=True)
        return serializer.data 