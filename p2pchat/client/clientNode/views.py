#views.py
from clientNode import *
from files import RegistrationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from uuid import getnode as get_mac
import json
import requests
 
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST) # A form bound to the POST data
        url='http://127.0.0.1:8010'
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

def checkValidEmail(request):
    url='http://localhost:8010/checkvalidemail'
    dataq=dataq={'emailid': request.POST['name']}
    r=requests.get(url,data=dataq)
    return HttpResponse("122")
