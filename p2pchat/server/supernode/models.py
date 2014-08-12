from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
import datetime
import collections

connected_user_list = {}

user_last_seen = collections.OrderedDict()  #dictionary to store last seen time of users.
user_last_seen_invert = {}


class UserData(User):
	mac_id=models.CharField(max_length=17)
	ip_address=models.CharField(max_length=39)
	roll_no=models.CharField(max_length=20)
	college_name=models.CharField(max_length=30)
	onlineinfo=models.BooleanField(default=1)
	objects=UserManager()
	
	def __str__(self):
		return "roll_no:{0} mac_id:{1} status:{2} email:{3} ".format(self.roll_no,self.mac_id,self.onlineinfo,self.email)


	def add_to_online_list(self):
			global connected_user_list
			connected_user_list[self.username] = self.ip_address   #the list contains email - ip_address pairs of all online users
			global user_last_seen
			global user_last_seen_invert
			user_last_seen[self.username] = (datetime.datetime.now(),self.ip_address)
			user_last_seen_invert[self.ip_address] = self.username

@receiver(post_save,sender=UserData)
def user_online_status_changed(sender,**kwargs):
	obj = kwargs['instance'] # obj is the object which has been saved/updated
	global connected_user_list

	if obj.onlineinfo == 'False'and connected_user_list.has_key(obj.username):
		del connected_user_list[obj.username]
		dataq = {'username':obj.username}
		for username_id in connected_user_list:
			url = connected_user_list[username]+'/offlineinfo'# make changes
			requests.post(url,data=json.dumps(dataq))
		
	elif obj.onlineinfo == 'True' and not connected_user_list.has_key(obj.username):
		connected_user_list[obj.username] = obj.ip_address
		dataq = {'username':obj.username}
		for username_id in connected_user_list:
			url = connected_user_list[username]+'/onlineinfo'# make changes
			requests.post(url,data=json.dumps(dataq))

	else:
		pass