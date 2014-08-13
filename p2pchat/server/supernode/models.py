from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
import datetime
import collections
import json

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
			print "in add to online list *******"
			connected_user_list[self.username] = self.ip_address   #the list contains email - ip_address pairs of all online users
			print connected_user_list
			print "---------"
			global user_last_seen
			global user_last_seen_invert
			user_last_seen[self.username] = (datetime.datetime.now(),self.ip_address)
			print "''''''''"
			print user_last_seen
			print "******"
			user_last_seen_invert[self.ip_address] = self.username
			print user_last_seen_invert

@receiver(post_save,sender=UserData)
def user_online_status_changed(sender,**kwargs):
	print "in signal recievr"
	obj = kwargs['instance'] # obj is the object which has been saved/updated
	print obj
	global connected_user_list
	print connected_user_list
	print obj.onlineinfo
	print "****"
	print obj.username
	print "***"

	if obj.onlineinfo == False and connected_user_list.has_key(obj.username):
		del connected_user_list[obj.username]
		dataq = {'username':obj.username}
		print "in if of receiver"
		for username_id in connected_user_list:
			print "in offline message sent"
			url =  "http://"+connected_user_list[username_id]+':8000/offlineinfo'# make changes
			r=requests.get(url,data=json.dumps(dataq))
			print r.text
		
	elif obj.onlineinfo == True and not connected_user_list.has_key(obj.username):
		connected_user_list[obj.username] = obj.ip_address
		dataq = {'username':obj.username}
		print "in elseif of receiver"
		print connected_user_list
		for username_id in connected_user_list:
			print "in online message sent"
			url = "http://"+connected_user_list[username_id]+':8000/onlineinfo'# make changes
			print url
			r=requests.get(url,data=json.dumps(dataq))
			print r.text

	else:
		pass
