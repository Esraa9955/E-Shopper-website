from rest_framework import serializers
from .models import Order, OrderItem
from product.serlizer import ProductsSerlizer
from cart.models import Cart

from django.db import transaction
#from user_profile.serializers import AddressSerializer, UserMiniSerializer
#from products.serializers import ProductDetailSerializer


        

class OrderItemSerializer(serializers.ModelSerializer):
    product=ProductsSerlizer()
    class Meta:
        model= OrderItem
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items=OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id =self.context["user_id"]
            order=Order.objects.create(buyer_id=user_id)
            cartitems = Cart.objects.filter(cart_id=cart_id)
            orderitems =[
                OrderItem(order=order,
                        product=item.product,
                        quantity=item.quantity
                        )
                for item in cartitems
            ]
            OrderItem.objects.bulk_create(orderitems)
            Cart.objects.filter(id=cart_id).delete()



#class OrderMiniSerializer(serializers.ModelSerializer):
#    address = AddressSerializer(required=False)
#    buyer = UserMiniSerializer(required=False)

#    class Meta:
#        model = Order
#        exclude = "modified"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = "modified"


class OrderItemMiniSerializer(serializers.ModelSerializer):
#    order = OrderMiniSerializer(required=False, read_only=True)
    #product = ProductDetailSerializer(required=False, read_only=True)

    class Meta:
        model = OrderItem
        exclude = "modified"