from django.db import models
from product.models import Product
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

    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    order_number = models.CharField(max_length=250, blank=True, null=True)
    is_paid = models.BooleanField(default=False)

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