from rest_framework import serializers
from cart.models import *


class CartSerlizer(serializers.ModelSerializer):
    def validate(self, data):
        if Cart.objects.filter(user=data['user'], item=data['item']).exists():
            raise serializers.ValidationError({'errmsg':"You have already added this item to your cart."})
        else:
            if data['user'].usertype != 'customer':
                raise serializers.ValidationError({'errmsg':"user isn't a customer"})
            else:
                if data['quantity'] > data['item'].stock:
                    raise serializers.ValidationError({'errmsg':"more than stock"})
        return data
    class Meta:
        model = Cart
        fields = '__all__'



    def create(self, validated_data):
        # ** means 3aml el validate data k dict
        return Cart.objects.create(**validated_data)
