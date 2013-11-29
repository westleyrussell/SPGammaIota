from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

def home(request):
	""" View for the index landing page of the site """
	context = RequestContext(request,{
		'motd': 'drob rules',
		'title': 'Secure'
	})
	return render(request,'secure_home.html',context)
