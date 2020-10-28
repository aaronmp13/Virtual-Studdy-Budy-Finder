from django.db import models

# Create your models here.

class Profile(models.Model):
	username = models.CharField(max_length=20, default="User X")
	name = models.CharField(max_length=50, default="Name X")
	gender = models.CharField(max_length=200, default="Gender X")
	major = models.CharField(max_length=200, default="Major X")
	age = models.IntegerField(default = 0)
	description = models.CharField(max_length=2000, default="Description X")
	picture = models.ImageField(upload_to='uploads/')

	def __str__(self):
		return self.username, self.name, self.gender, self.major, str(self.age), self.description
