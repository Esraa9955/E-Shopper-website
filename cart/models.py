from django.db import models
from django.conf import settings
from product.models import Product

class Cart(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True,)
  # ordered = models.BooleanField(default=False)
  item = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,)
  quantity = models.IntegerField(default=1)
  # total_cost = models.DecimalField(default=0,decimal_places=2,max_digits=6)
  # sub_cost = models.DecimalField(default=0,decimal_places=2,max_digits=6)

  def __str__(self):
        return f"{self.quantity} of {self.item.name}"

  def get_total_item_price(self):
      return self.quantity * self.item.price