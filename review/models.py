from django.db import models
from product.models import Product
# from users.models import Admin
import datetime
class Review(models.Model):
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  # customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
  # admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE)
  comment= models.TextField(max_length=1000)
  date = models.DateField(default=datetime.datetime.today)

  

