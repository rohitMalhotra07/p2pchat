from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import json

def chat(request):	
	variables = RequestContext(request, {})
	return render_to_response('chat.html',variables)