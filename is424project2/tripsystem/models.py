from django.db import models

# Create your models here.
class Trip(models.Model):
    source = models.CharField(max_length = 64)
    destination = models.CharField(max_length=64)
    time= models.CharField(max_length=64, default="N/A")
    capacityLeft = models.IntegerField(default=30)

class User(models.Model):
    username = models.CharField(max_length = 64,primary_key=True)
    password = models.CharField(max_length = 64)
    trip = models.ManyToManyField(Trip, blank=True, related_name="users")