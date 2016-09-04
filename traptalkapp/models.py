from django.db import models


class User(models.Model):
	username = models.CharField(max_length=15)
	password = models.CharField(max_length=200)
	token = models.CharField(max_length=200)

	def __str__(self):
		return 'User is: ' + self.username


class ValidTokens(models.Model):
	token = models.CharField(max_length = 50)
	validFor = models.ForeignKey('User', on_delete=models.CASCADE)
	issued = models.DateTimeField(auto_now_add=True, blank=True)