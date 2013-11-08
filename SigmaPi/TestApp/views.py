# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from TestApp.models import Status
from django

def index(request):
	context = RequestContext(request, {
			'error_msg' : "Not Authenticated",
			'form' : LoginForm()
		})

	if request.user.is_authenticated():
		status_list = Status.objects.filter(user=request.user)
		context = RequestContext(request, {
			'status_list' : status_list,
			})

	return render(request, 'status/index.html', context)

def logout_view(request):
	logout(request)

	return index(request)

def login_view(request):
	return request
