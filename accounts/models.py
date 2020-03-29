from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class extendedUser(models.Model):
    user = models.OneToOneField(User, on_delete= models.PROTECT,null = True, related_name= "extendedUser")
    user_status_choices = [
        (1, 'Coronora Virus Positive'),
        (2,'Shows Symptoms'),
        (3,'Travel History Abroad'),
        (4,'Close Contact'),
        (5,'Normal User'),
    ]
    status = models.IntegerField(choices= user_status_choices,blank= True, null= True)
    is_admin = models.BooleanField(default= False)
    def __str__(self):
        return self.user.username + "'s extended user class"
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        my_extended_user = extendedUser(user = instance)
        my_extended_user.save()
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.extendedUser.save()