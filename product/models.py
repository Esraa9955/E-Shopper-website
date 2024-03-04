from django.db import models
from category.models import Category
from django.conf import settings
from django.core.exceptions import ValidationError


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
    ratings = models.DecimalField(max_digits=3,decimal_places=2,default=0)
    new = models.BooleanField(default=False)
    sale = models.BooleanField(default=False)
    newprice = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    thumbnail = models.ImageField(upload_to='product/images/', default='static/images/notfound.png')
    images = models.ManyToManyField('ProductImage', related_name='products', blank=True)

    def clean(self):
        super().clean()
        if self.sale and self.newprice >= self.price:
            raise ValidationError("New price must be less than the original price if the product is on sale.")

class ProductImage(models.Model):
    image = models.ImageField(upload_to='product/images/',default='static/images/notfound.png')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name
    

class Rates(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE,related_name='rates')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(default=0)
    createAt = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.rating