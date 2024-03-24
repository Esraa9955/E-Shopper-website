from rest_framework import serializers
from product.models import *



class ProductsSerlizer(serializers.ModelSerializer):
    rates = serializers.SerializerMethodField(method_name='get_rates',read_only=True)


    class Meta:
        model = Product
        fields='__all__'
       
       
    def get_rates(self,obj):
        rates = obj.rates.all()
        serializer = RateSerializer(rates,many=True)
        return serializer.data

  

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
        instance.ratings=validated_data.get('ratings')
        instance.new=validated_data.get('new')
        instance.sale=validated_data.get('sale')
        instance.sizeable=validated_data.get('sizeable')
        instance.newprice=validated_data.get('newprice')
        instance.stock_S=validated_data.get('stock_S')
        instance.stock_M=validated_data.get('stock_M')
        instance.stock_L=validated_data.get('stock_L')
        instance.stock_XL=validated_data.get('stock_XL')
        instance.subImageOne=validated_data.get('subImageOne')
        instance.subImageTwo=validated_data.get('subImageTwo')
        instance.subImageThree=validated_data.get('subImageThree')
        instance.subImageFour=validated_data.get('subImageFour')
        instance.save()
        return instance   

    
class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rates
        fields = "__all__"


