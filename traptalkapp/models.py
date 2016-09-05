from django.db import models


class User(models.Model):
	username = models.CharField(max_length=15)
	password = models.CharField(max_length=200)


class ValidToken(models.Model):
	token = models.CharField(max_length = 50)
	validFor = models.ForeignKey('User', on_delete=models.CASCADE)
	issued = models.DateTimeField(auto_now_add=True, blank=True)


class Friend(models.Model):
	friend_one = models.ForeignKey('User', related_name = 'adder', on_delete = models.CASCADE)
	friend_two = models.ForeignKey('User', related_name = 'addee',  on_delete = models.CASCADE)
	since = models.DateTimeField(auto_now_add=True, blank=True)


class Message(models.Model):
	message_from = models.ForeignKey('User',  related_name = 'sender', on_delete = models.CASCADE)
	message_to = models.ForeignKey('User', related_name = 'sendee',  on_delete = models.CASCADE)
	sent = models.DateTimeField(auto_now_add=True, blank=True)
	message_contents = models.CharField(max_length = 1000)
	
class Meta:
        managed = True	