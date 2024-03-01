from rest_framework import serializers
from product.models import *

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)

class ProductsSerlizer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    images = serializers.PrimaryKeyRelatedField(many=True, queryset=ProductImage.objects.all())

    reviews = serializers.SerializerMethodField(method_name='get_rates',read_only=True)


    class Meta:
        model = Product
        fields = '__all__'
       
    def get_rates(self,obj):
        rates = obj.rates.all()
        serializer = RateSerializer(rates,many=True)
        return serializer.data

    def create(self, validated_data):
        images_data = validated_data.pop('images', []) 
        product = Product.objects.create(**validated_data)
        product.images.set(images_data)
        return product

    def create(self, validated_data):
         #** means 3aml el validate data k dict
        return Product.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.image= validated_data.get('image')
        instance.description = validated_data.get('description')
        instance.price = validated_data.get('price')
        instance.add_date = validated_data.get('add_date')
        instance.update_date= validated_data.get('update_date')
        instance.brand = validated_data.get('brand')
        instance.stock= validated_data.get('stock')
        instance.save()
        return instance   

    def create(self, validated_data):
        images_data = validated_data.pop('images', []) 
        product = Product.objects.create(**validated_data)
        product.images.set(images_data)
        return product


    def create(self, validated_data):
     images_data = validated_data.pop('images', []) 
     product = Product.objects.create(**validated_data)

    
     for image_data in images_data:
        ProductImage.objects.create(product=product, **image_data)

     return product

class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rates
        fields = "__all__"


