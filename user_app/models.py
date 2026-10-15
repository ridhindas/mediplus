from django.db import models

# Create your models here.

class appointment_details(models.Model):
    userid=models.CharField(max_length=12)
    patientname=models.CharField(max_length=200)
    patientage=models.CharField(max_length=200)
    patientemail=models.CharField(max_length=200)
    patientphone=models.CharField(max_length=200)
    docname=models.CharField(max_length=200)
    bookingdate=models.CharField(max_length=200)
    patientproblem=models.CharField(max_length=200)
