from django.db import models


class User(models.Model):
	mac_id=models.CharField(max_length=17)
	ip_address=models.CharField(max_length=39)
	first_name = models.CharField(max_length=30)
	email = models.CharField(max_length=35,primary_key=True)
	roll_no=models.CharField(max_length=20)
	password=models.CharField(max_length=20)
	college_name=models.CharField(max_length=30)

	def __str__(self):
		return self.first_name