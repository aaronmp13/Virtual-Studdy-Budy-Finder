from django.db import models
from django.core.validators import *

# Create your models here.

class Profile(models.Model):
	username = models.CharField(max_length=20, default="")
	name = models.CharField(max_length=50, default="", validators = [MinLengthValidator(1), MaxLengthValidator(50)])
	gender = models.CharField(max_length=200, default="", validators = [MinLengthValidator(1), MaxLengthValidator(200)])
	major = models.CharField(max_length=200, default="", validators = [MinLengthValidator(1), MaxLengthValidator(200)])
	age = models.IntegerField(default = 0, validators = [MinValueValidator(1), MaxValueValidator(100)])
	description = models.CharField(max_length=2000, default="", validators = [MinLengthValidator(1), MaxLengthValidator(2000)])
	coursework = models.CharField(max_length=2000, default="", validators = [MinLengthValidator(1), MaxLengthValidator(2000)])
	classOf = models.IntegerField(default = 2023, validators = [MinValueValidator(2020), MaxValueValidator(2024)])
	picture = models.ImageField(upload_to='uploads/', validators=[validate_image_file_extension], blank=True)
	matches = []
	matches_emails=[]

	def __str__(self):
		return self.username + " " + self.name + " " + self.gender + " " + self.major + " " + str(self.age) + " " + self.description + " " + self.coursework + " " + str(self.classOf)
