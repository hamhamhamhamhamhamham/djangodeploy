from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
# Create your models here.



class Product(models.Model):
    def __str__(self):
        return self.name
   
    def get_absolute_url(self):
        return reverse("my_papp:products")
    
    # ** default seller of products before this field is user with ID 1 -> hamidreza
    # ** seller_name is User object which shows -> user name by def--> __str__ ...
    seller_name = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    name= models.CharField(max_length=50)
    price= models.FloatField()
    desc=models.CharField(max_length=200)
    image =models.ImageField(blank=True,upload_to="images")
    create_date = models.DateTimeField(auto_now_add=True)




class OrderDetaile(models.Model) :
    customer_username = models.CharField(max_length=100)
    # user Product datas in Order!
    # when order is deleted product won't
    product = models.ForeignKey(to='Product',on_delete=models.PROTECT)
    amount = models.FloatField()
    stripe_payment_intent = models.CharField(max_length=200)
    has_paid= models.BooleanField(default=False)
    # set value auto
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now_add=True)
