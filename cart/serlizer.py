from rest_framework import serializers
from cart.models import *


class CartSerlizer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'



    def create(self, validated_data):
        # ** means 3aml el validate data k dict
        return Cart.objects.create(**validated_data)
    

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name')
    #     instance.image= validated_data.get('image')
    #     instance.description = validated_data.get('description')
    #     instance.price = validated_data.get('price')
    #     instance.add_date = validated_data.get('add_date')
    #     instance.update_date= validated_data.get('update_date')
    #     instance.brand = validated_data.get('brand')
    #     instance.stock= validated_data.get('stock')
    #     instance.save()
    #     return instance    
