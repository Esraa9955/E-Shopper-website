from django.db import models
from cart.models import Cart
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator


# class Admin(models.Model):
#   name=models.CharField(max_length=50)
#   password=models.CharField(max_length=100)
#   role=models.CharField(max_length=50)


# class User(AbstractUser):
#   username=models.CharField(max_length=255, unique=True)
#   first_name=models.CharField(max_length=255)
#   last_name=models.CharField(max_length=255)
#   email=models.EmailField(max_length=255, unique=True)
#   password=models.CharField(max_length=255)
#   confirm_password=models.CharField(max_length=255,default='')
#   shopname = models.CharField(max_length=255, blank=True)
#   phone = models.CharField(max_length=15, default=None)
#   USER_TYPE_CHOICES = [
#         ('customer', 'Customer'),
#         ('vendor', 'Vendor'),
#     ]
#   usertype = models.CharField(max_length=20, choices=USER_TYPE_CHOICES,default="customer")

#   REQUIRED_FIELDS = []
  # USERNAME_FIELD = 'username'

# class Vendor(models.Model):
#   admin_id=models.ForeignKey(Admin,on_delete=models.CASCADE)
#   Name=models.CharField(max_length=100)
#   email=models.EmailField(max_length=100)
#   phone=models.CharField(max_length=50)
#   payment_terms=models.CharField(max_length=200)
#   contact_person=models.CharField(max_length=200)


# class DeliveryMan(models.Model):
#   name=models.CharField(max_length=100)
#   phone=models.CharField(max_length=50)

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    ]

    first_name = models.CharField(max_length=10, blank=True, validators=[MinLengthValidator(limit_value=3), MaxLengthValidator(limit_value=30)])
    last_name = models.CharField(max_length=10, blank=True, validators=[MinLengthValidator(limit_value=3), MaxLengthValidator(limit_value=30)])
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255 , default='')
    username = models.CharField(max_length=25 , default='')
    USERNAME_FIELD = 'email'
    phone = models.CharField(max_length=11)
    usertype = models.CharField(choices=USER_TYPE_CHOICES)
    address = models.CharField(max_length=100, default='')
    shopname = models.CharField(max_length=100, blank=True, null=True)
    birthdate=models.DateField(null=True)
    
    REQUIRED_FIELDS = ['first_name', 'last_name','username']


    @classmethod
    def usersList(self):
        return self.objects.all()
    
   