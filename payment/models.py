from django.db import models
from order.models import Order
# from users.models import Customer,Vendor

import datetime
class Payment(models.Model):
  date = models.DateField(default=datetime.datetime.today)
  method = models.CharField(max_length=50)
  status = models.BooleanField(default=False)

class PaymentOrder(models.Model):
  #order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
  payment_id=models.ForeignKey(Payment,on_delete=models.CASCADE)
  # Customer_id =models.ForeignKey(Customer,on_delete=models.CASCADE)

class PaymentVendor(models.Model):
  # vendor_id=models.ForeignKey(Vendor,on_delete=models.CASCADE)
  payment_id=models.ForeignKey(Payment, on_delete=models.CASCADE)
  plan=models.TextField(max_length=1000)