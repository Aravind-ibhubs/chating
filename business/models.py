from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.  

Department = (
    ("Job Seekers" ,"Job"),
    ("Employers" ,"Employers"),
    ("Sales_Department" ,"Sales"),
    ("HR_Department" ,"HR"),
    ("Developers" ,"Coders"),
    ("Staff" ,"Staff")
)  

class User(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)  
    departmant = models.CharField(max_length=20, choices=Department, default="Staff") 
    
    def __str__(self):
        return self.first_name + self.last_name

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Chat(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    msg_receiver = models.CharField(max_length=60)
    
    def __str__(self):
        return self.message_id

class Jobs(models.Model):
    job_id = models.AutoField(primary_key=True)
    post = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    rating = models.IntegerField()
    description = models.TextField(max_length=220)
    posted_on = models.DateField(auto_now=True)
    
    def __str__(self):
        return str(self.job_id) + ")" + self.post

