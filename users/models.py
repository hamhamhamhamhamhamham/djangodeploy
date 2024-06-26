from django.db import models
# this is User Model(in forms.py)
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    # connect Profile model To User Model >> FK or OneToOneField

    def __str__(self):
        return self.user.username
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   
    image = models.ImageField(default="profile.jpg",upload_to="profile_images")
    contact_number = models.CharField(max_length=100,default="999999999")