from django.shortcuts import render
from django.http import HttpResponse
import json
from django.shortcuts import render_to_response
from django.template import Template, RequestContext
from django import template
from django.template import Context
from django.http import QueryDict
import requests
from supernode.models import UserData
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
import threading
import datetime
import time
import bisect    # for implementing binary search in user_last_seen
import collections   # for ordered dictionary
from supernode.models import UserData
from supernode.models import user_last_seen , user_last_seen_invert

class OnlineStatusUpdate(threading.Thread):   #thread to update the user_connected_status after each 10 seconds
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while 1:
			global user_last_seen
			print "in online status update thread"
			index = bisect.bisect_right(tuple(x[0] for x in user_last_seen.values()),datetime.datetime.now()-datetime.timedelta(seconds=50))  #calculates the index of last user who is online. Every user after him is onlne and before him is offline.
			for i in range(index-1):
				obj = UserData.objects.get(username = user_last_seen.keys()[i])
				if obj.onlineinfo !=False:
					obj.onlineinfo =False
					obj.save()
			for i in range(len(user_last_seen)-index+1):
				obj = UserData.objects.get(username = user_last_seen.keys()[index+i])
				if obj.onlineinfo!=True:
					obj.onlineinfo =True
					obj.save()
			time.sleep(100)

online_status_update = OnlineStatusUpdate()

def connectedcheck(request):
	print "in connected check"
	global user_last_seen
	global user_last_seen_invert
	data=json.loads(request.body)
	print data['messagetime']
	if data.has_key('messagetime'):
		print "in if of connected check"
		ip = get_client_ip(request)   # get the ip address of the client
		print user_last_seen_invert 
		username = user_last_seen_invert[ip]   #get the email id corresponding to that ip address
		print username
		del user_last_seen[username]
		print user_last_seen
		user_last_seen[username] = (datetime.datetime.strptime(data['messagetime'],"%Y-%m-%d %H:%M:%S.%f"),ip)   # update the last seen time of the user in the user_last_seen dict
		return HttpResponse("reached")
	else:
		return HttpResponse("not reached")

class MyCustomBackend:
	def authenticate(self, username=None, password=None,tempmac=None):
		print "in authenticate"
		print username,password,tempmac
		try:
			temp=UserData.objects.get(username=username)
			print temp.password
			if str(temp.password)==str(password):
				if str(tempmac)==str(temp.mac_id):
					temp.is_active=True
					temp.save()
					return temp
				else:
					print tempmac
					print temp.mac_id
					return None
			else:
				return None
		except User.DoesNotExist:
			return None
		def get_user(self, Username):
			try:
				return UserData.objects.get(username=Username)
			except User.DoesNotExist:
				return None 

mac_id_hashtable={}

def user_registration(request):
	print 'here'
	data = json.loads(request.body)
	ip_address=get_client_ip(request)
	print ip_address
	print data['mac_address']
	print data['username']
	print data['password']
	u=UserData.objects.create(username=data['username'],email=data['email'],password=data['password'],mac_id=data['mac_address'],ip_address=ip_address,roll_no= data['roll_no'],college_name=data['college_name'],onlineinfo=False)
	#u.add_to_online_list()
	print "done1"
	#tempuserdata=UserData.objects.create(mac_id=data['mac_address'],ip_address=ip_address,roll_no= ['roll_no'],college_name=data['college_name'],onlineinfo=0)
	print 'done2'
	#print User.objects.all()
	print u.mac_id
	global online_status_update
	if not online_status_update.isAlive():
		print "online online_status_update started"
		online_status_update.start()
	return HttpResponse("SUCCESS")



def make_hash():
	all_entries = Entry.objects.all()
	global mac_id_hashtable
	
	for user in all_entries:
		mac_id=user.mac_id
		mac_id_hashtable[mac_id]=1

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


def checkvalidusername(request):
	print "request to check valid username recieved"
	data=json.loads(request.body)
	print data
	if data.has_key('username'):
		Username=data['username']
		num_results = UserData.objects.filter(username=Username).count()
		print num_results
		if num_results==0:
			datasend={'value':'True'}
			return HttpResponse(json.dumps(datasend))
		else:
			datasend={'value':'False'}
			return HttpResponse(json.dumps(datasend))
	else:
		datasend={'value':'no username recieved'}
		return HttpResponse(json.dumps(datasend))

def logincheck(request):
	print 'In login check'
	data=json.loads(request.body)
	username = data['username']
	password = data['password']
	mac_address=data['mac_address']
	user = authenticate(username=username, password=password,tempmac=mac_address)
	print ">>>>"
	print user
	print "<<<<"
	if user is not None:
		if user.is_active:
			login(request, user)
			#print user.is_active
			user.onlineinfo=True
			print "in login check before user save"
			user.save()
			print "in login check after user save"
			user.add_to_online_list()
			#print user.onlineinfo
			#tempdata=getonlinelist()
			tempdata={'value':'logged in'}
			return HttpResponse(json.dumps(tempdata))
		else:
			tempdata={'value':'disabled account'}
			return HttpResponse(json.dumps(tempdata))
	else:
		tempdata={'value':'invalid login'}
		return HttpResponse(json.dumps(tempdata))

def recieveonlinelist(request):
	u=UserData.objects.filter(onlineinfo=True)
	print u.count()
	data={}
	data['onlinelist']=list()
	print data
	for item in u:
		tempname=item.username
		tempip=item.ip_address
		data['onlinelist'].append({'username':tempname,
									'ip_address':tempip
								  })
		print tempname
	print data
	return HttpResponse(json.dumps(data))

def logoutServer(request):
	print "in logout"
	data=json.loads(request.body)
	username=data['username']
	#print username
	u=UserData.objects.get(username=username)
	u.onlineinfo=False
	u.is_active=False
	u.save()
	#print u
	#logout(username)
	return HttpResponse("done logging out")
"""
def clientToServerPolling(request):
	print "request to poll recieved"
	data=json.loads(request.body)
	tempusername=data['username']
	tempip=get_client_ip(request)
	response={}
	n=UserData.objects.filter(username=tempusername).count()
	if n!=0:
		u=UserData.objects.get(username=tempusername)
		u.onlineinfo=True
		u.ip_address=tempip
		response['value']="updated"
		return HttpResponse(json.dumps(response))
	else:
		response['value']="not updated"
		return HttpResponse(json.dumps(response))
"""