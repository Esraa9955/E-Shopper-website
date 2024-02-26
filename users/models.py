from django.db import models
from cart.models import Cart
class Admin(models.Model):
  name=models.CharField(max_length=50)
  password=models.CharField(max_length=100)
  role=models.CharField(max_length=50)

class Customer(models.Model):
  fist_name=models.CharField(max_length=50)
  last_name=models.CharField(max_length=50)
  email=models.EmailField(max_length=100)
  password=models.CharField(max_length=100)
  phone=models.CharField(max_length=100)
  cart_id=models.ForeignKey(Cart, on_delete=models.CASCADE)
  #address

class Vendor(models.Model):
  admin_id=models.ForeignKey(Admin,on_delete=models.CASCADE)
  Name=models.CharField(max_length=100)
  email=models.EmailField(max_length=100)
  phone=models.CharField(max_length=50)
  payment_terms=models.CharField(max_length=200)
  contact_person=models.CharField(max_length=200)


class DeliveryMan(models.Model):
  name=models.CharField(max_length=100)
  phone=models.CharField(max_length=50)