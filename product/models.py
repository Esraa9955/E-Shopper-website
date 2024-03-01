from django.db import models
from category.models import Category
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,default="",blank=False)
    category= models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/images/', default='static/images/notfound.png')
    description = models.TextField(max_length=1000,default="",blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    add_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True,null=True, blank=True)
    brand = models.CharField(max_length=225,default="",blank=False)
    stock=models.IntegerField(default=0)
  

    thumbnail = models.ImageField(upload_to='product/images/', default='static/images/notfound.png')
    images = models.ManyToManyField('ProductImage', related_name='products', blank=True)

class ProductImage(models.Model):
    image = models.ImageField(upload_to='product/images/',default='static/images/notfound.png')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name