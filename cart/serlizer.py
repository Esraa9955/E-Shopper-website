from rest_framework import serializers
from cart.models import *


class CartSerlizer(serializers.ModelSerializer):
    item_image = serializers.ImageField(source='item.image', read_only=True)
    def validate(self, data):
        user = self.context['request'].user
        item = data.get('item')
        quantity = data.get('quantity')

        # Check if the user is a customer
        if user.usertype != 'customer':
            raise serializers.ValidationError({'error': "User isn't a customer."})

        # Check if the quantity is valid
        if quantity <= 0:
            raise serializers.ValidationError({'error': "Quantity must be greater than zero."})

        # Check if the quantity exceeds the item stock
        if item and quantity > item.stock:
            raise serializers.ValidationError({'error': "Quantity exceeds stock."})

        return data
    class Meta:
        model = Cart
        fields = '__all__'



    def create(self, validated_data):
        return Cart.objects.create(**validated_data)
    
