from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
import requests
import json
import threading
import datetime
import time

import redis

ServerAddress="http://127.0.0.1:8010"
class IsOnline(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.signal=True

    def run(self):
    	while self.signal==True:
    		runthread()
    def stop(self):
    	self.signal=False

def runthread():
	global ServerAddress
	currenttime=str(datetime.datetime.now())
	checkmessage = {'messagetime':currenttime}
	print checkmessage
	r = requests.get(ServerAddress+'/connectedcheck',data=json.dumps(checkmessage))#can use get() if we want some response from server
	#print (r.text)
	time.sleep(50)

poll=IsOnline()

@csrf_exempt
def recieve_offline_info(request):
    try:
        #Get User from from request       
        #Once comment has been created post it to the chat channel
        print "received offline info for"
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        data_received=json.loads(request.body)
        print data_received
        data={'username':data_received['username'],
        'value':'offline'}
        message=json.dumps(data)
        r.publish('onlineOfflineinfo',message)        
        return HttpResponse("Everything worked :)")
    except:
    	print "in Exception"
        return HttpResponse()

def recieve_online_info(request):
	try:
		print "received online info for"
		r = redis.StrictRedis(host='localhost', port=6379, db=0)
		data_received=json.loads(request.body)
		data={'username':data_received['username'],
		'value':'online'}
		message=json.dumps(data)
		r.publish('onlineOfflineinfo',message)        
		return HttpResponse("Everything worked :)")
	except :
		print "in Exception"
		return HttpResponse("not worked")

def recieve_list(request):
	print("entered recieve list")
	url=ServerAddress+'/recieveonlinelist'
	data={}
	r = requests.get(url) #give username with this request to ensure useris logged in.
	data_received=json.loads(r.text)
	getonlinelist(data_received)
	global poll
	poll.start()
	return HttpResponse(json.dumps(data_received))



def getonlinelist(data_received):
    for item in data_received['onlinelist']:
    	print item['username']
        tempusername=item['username']
        tempip=item['ip_address']
    print data_received


