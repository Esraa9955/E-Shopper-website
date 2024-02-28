from django.db import models
from product.models import Product
from django.contrib.auth.models import User
# from users.models import DeliveryMan  # Uncomment this line if needed
import datetime
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class Order(models.Model):
  PENDING_STATE = 'P'
  SHIPPED_STATE = 'S'
  DELIVERED_STATE = 'D'
  ORDER_STATUS_CHOICES = [
      (PENDING_STATE, "pending"),
      (SHIPPED_STATE, "shipped"),
      (DELIVERED_STATE, "delivered")
  ]

  buyer =  models.ForeignKey(UserModel,related_name="order", on_delete=models.CASCADE)
  order_number = models.CharField(max_length=250, blank=True, null=True)
  #delivery_man_id = models.ForeignKey(DeliveryMan,on_delete=models.CASCADE)
  #payment_method = models.ForeignKey(Payment,on_delete=models.CASCADE)
  placed_at= models.DateField(auto_now_add=True)
  status = models.CharField(
        max_length=50, choices=ORDER_STATUS_CHOICES, default=PENDING_STATE
    )
  is_paid = models.BooleanField(default=False)
  #address = models.ForeignKey(
  #      Address, related_name="order_address", on_delete=models.CASCADE
  #  )

    




  @staticmethod
  def create_order(buyer, order_number, address, is_paid=False):
      order = Order()
      order.buyer = buyer
      order.order_number = order_number
      order.is_paid = is_paid
      order.save()
      return order

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="product_order", on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    total_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    @staticmethod
    def create_order_item(order, product, quantity, total):
        order_item = OrderItem()
        order_item.order = order
        order_item.product = product
        order_item.quantity = quantity
        order_item.total_price = total  # Fixing the attribute name
        order_item.save()
        return order_item
    


