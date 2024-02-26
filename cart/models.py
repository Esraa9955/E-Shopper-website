from django.db import models

class Cart(models.Model):
  quantity = models.IntegerField(default=1)
  total_cost = models.DecimalField(default=0,decimal_places=2,max_digits=6)
  sub_cost = models.DecimalField(default=0,decimal_places=2,max_digits=6)