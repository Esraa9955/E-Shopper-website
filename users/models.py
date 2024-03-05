from django.db import models
from cart.models import Cart
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator,RegexValidator
from django.contrib.auth.hashers import make_password


# class Admin(models.Model):
#   name=models.CharField(max_length=50)
#   password=models.CharField(max_length=100)
#   role=models.CharField(max_length=50)

# class DeliveryMan(models.Model):
#   name=models.CharField(max_length=100)
#   phone=models.CharField(max_length=50)

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    ]

    first_name = models.CharField(max_length=10, validators=[MinLengthValidator(limit_value=3), MaxLengthValidator(limit_value=30)])
    last_name = models.CharField(max_length=10,  validators=[MinLengthValidator(limit_value=3), MaxLengthValidator(limit_value=30)])
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    confirmPassword = models.CharField(max_length=255 )
    username = models.CharField(max_length=25 , default='')
    USERNAME_FIELD = 'email'
    phone = models.CharField(max_length=13, validators=[RegexValidator(regex=r'^\+201\d{9}$', message='Invalid phone number', code='invalid_phone')], blank=True)
    usertype = models.CharField(choices=USER_TYPE_CHOICES)
    address = models.CharField(max_length=100, default='')
    shopname = models.CharField(max_length=100,blank=True,default='')
    birthdate=models.DateField(null=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    
    REQUIRED_FIELDS = ['first_name', 'last_name','username']


    @classmethod
    def usersList(self):
        return self.objects.all() 
    
    def save(self, *args, **kwargs):
        # Hash the confirmPassword field and save it as the password
        if self.confirmPassword:
            self.password = make_password(self.confirmPassword)
        super().save(*args, **kwargs)
   