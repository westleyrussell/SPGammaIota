from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.
def users(request):
	users = User.objects.all()
	context = RequestContext(request, {
		'all_users': users,
		})
	return render(request, 'users.html', context)

def single_user(request, user):
	requested_user = User.objects.get(username__exact=user)
	context = RequestContext(request, {
			'requested_username': user,
			'requested_user': requested_user
		})
	return render(request, 'user.html', context)

def profile(request):
	if request.user.is_active:
		return single_user(request, request.user.username)
	else:
		return HttpResponse("Not Authenticated")