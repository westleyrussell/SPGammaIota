from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.
def users(request):
	users = User.objects.all()

	output = "<br>".join([u.username for u in users])
	return HttpResponse(output)

def single_user(request, user):
	return HttpResponse(user)

def profile(request):
	output = "Not Authenticated"
	if request.user.is_active:
		output = request.user.username
	return HttpResponse(output)

