from django.db import models
from django.contrib.auth.models import User
class extendedUser(models.Model):
    user = models.OneToOneField(User, on_delete= models.PROTECT,null = True)
    user_status_choices = [
        (1, 'Coronora Virus Positive'),
        (2,'Shows Symptoms'),
        (3,'Travel History Abroad'),
        (4,'Close Contact'),
        (5,'Normal User'),
    ]
    status = models.IntegerField(choices= user_status_choices,blank= True, null= True)
    def __str__(self):
        return self.user.username + "'s extended user class"
# Create your models here.
