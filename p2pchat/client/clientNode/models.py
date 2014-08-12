from django.db import models
from django.contrib.auth.models import User

class messageTable(models.Model):
	message=models.TextField()
	fromname=models.CharField(max_length=39)
	toname=models.CharField(max_length=39)

#as a look up table
class messageMapping(models.Model):
	messageId=models.IntegerField()
	fromname=models.CharField(max_length=39)
	toname=models.CharField(max_length=39)

class OnlinePeople(models.Model):
	name=models.CharField(max_length=39)
	ip_address=models.CharField(max_length=39)
	onlineInfo=models.BooleanField(default=0)