from django.db import models
# from users.models import Admin

#categories of products
class Category(models.Model):
  name=models.CharField(max_length=255)
  parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
  # admin_id=models.ForeignKey(Admin,on_delete=models.CASCADE,default=1)

  def __str__(self):
    return self.name
