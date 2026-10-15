from django.db import models

# Create your models here.

class user_details(models.Model):
    userphoto=models.ImageField()
    username=models.CharField(max_length=200)
    useremail=models.CharField(max_length=200)
    userphone=models.CharField(max_length=12)
    userpassword=models.CharField(max_length=200)


    

class doctor_details(models.Model):
    docphoto=models.ImageField()
    docname=models.CharField(max_length=200)
    docspeciallization=models.CharField(max_length=200)
    docpayment=models.CharField(max_length=12)
    doctiming=models.CharField(max_length=200)