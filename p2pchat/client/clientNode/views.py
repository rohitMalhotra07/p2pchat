#views.py
from clientNode import *
from files import RegistrationForm 
from files import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from uuid import getnode as get_mac
import json
import requests

ServerAddress="http://172.16.64.71:8010"

def login(request):
    global ServerAddress
    if request.method=='POST':
        print 'we are here'
        form = LoginForm(request.POST) # A form bound to the POST data
        url=ServerAddress+'/logincheck'
        mac_address=get_mac()
        dataq={
            'email':request.POST['email'],
            'password':request.POST['password'],
            'mac_address':mac_address,
        }
        print dataq
        r = requests.get(url,data=json.dumps(dataq) )
        return HttpResponse(r)
    else:
        form =LoginForm()
        variables=RequestContext(request,
            {
                'form':form
            })
        return render_to_response('registration/login.html',variables,)

@csrf_exempt
def register(request):
    global ServerAddress
    if request.method == 'POST':
        form = RegistrationForm(request.POST) # A form bound to the POST data
        url=ServerAddress
        mac_address = get_mac()
        print 'reached here'
        dataq={
            'mac_address':mac_address,
            'name': request.POST['name'],
            'email':request.POST['email'],
            'roll_no':request.POST['roll_no'],
            'password':request.POST['password1'],
            'college_name': request.POST['college_name']
        }
        print dataq
        r = requests.get(url,data=json.dumps(dataq) )
        html = "<html><body> Success </body></html>"
        return HttpResponse(html)

    else:
        form = RegistrationForm()
        variables = RequestContext(request, 
            {
                'form': form 
            })
        return render_to_response(
        'registration/register.html',
        variables,
        )
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
def home(request):
    return render_to_response(
    'home.html',
    { 'user': request.user }
    )

def checkvalidemail(request):
    global ServerAddress
    url=ServerAddress+'/checkvalidemail'
    dataq={'emailid': request.POST.get('Email')}
    print dataq
    r=requests.get(url,data=json.dumps(dataq))

    return HttpResponse(r)
