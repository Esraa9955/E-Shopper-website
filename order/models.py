from django.db import models
from product.models import Product
# from users.models import DeliveryMan

import datetime
class Order(models.Model):
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  # customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
  # delivery_man_id = models.ForeignKey(DeliveryMan,on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)
  total_price = models.DecimalField(default=0,decimal_places=2,max_digits=6)
  #payment_method = models.ForeignKey(Payment,on_delete=models.CASCADE)
  date = models.DateField(default=datetime.datetime.today)
  status = models.BooleanField(default=False)

