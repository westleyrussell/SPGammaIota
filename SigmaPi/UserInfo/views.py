from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.
def users(request):
	users = User.objects.all()

	output = "<br>".join([u.username for u in users])
	return HttpResponse(output)

def single_user(request, user):
	requested_user = User.objects.get(username=user)
	context = RequestContext(request, {
			'requested_user': user,
			'user': requested_user
		})
	return render(request, 'user.html', context)

def profile(request):
	output = "Not Authenticated"
	if request.user.is_active:
		output = request.user.username
	return HttpResponse(output)