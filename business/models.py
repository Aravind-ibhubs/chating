from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.    

class User(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)   

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Chat(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    msg_receiver = models.CharField(max_length=60)

