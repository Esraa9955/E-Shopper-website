from django.db import models
from users.models import Admin

#categories of products
class Category(models.Model):
  name=models.CharField(max_length=255)
  admin_id=models.ForeignKey(Admin,on_delete=models.CASCADE,default=1)

  def __str__(self):
    return self.name
