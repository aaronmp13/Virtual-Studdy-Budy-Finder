from django.db import models

# Create your models here.

class Profile(models.Model):
	username = models.CharField(max_length=20, default="User X")
	name = models.CharField(max_length=50)
	gender = models.CharField(max_length=200)
	major = models.CharField(max_length=200)
	age = models.IntegerField(default=0)
	description = models.CharField(max_length=200, default="")
	picture = models.ImageField(upload_to='uploads/')

