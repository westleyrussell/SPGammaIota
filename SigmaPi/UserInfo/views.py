from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext

from UserInfo import utils
from UserInfo.models import UserInfo

# Create your views here.
def users(request):
	senior_year = utils.get_senior_year()

	# get the execs
#	sage = UserPosition.objects.get(position='S')
#	second = UserPosition.objects.get(position='2')
#	third = UserPosition.objects.get(position='3')
#	fourth = UserPosition.objects.get(position='4')
#	first = UserPosition.objects.get(position='1')
#	herald = UserPosition.objects.get(position='H')

	# get the rest
	seniors = UserInfo.objects.filter(graduationYear=senior_year).prefetch_related('user')
	juniors = UserInfo.objects.filter(graduationYear=(senior_year + 1)).prefetch_related('user')
	sophomores = UserInfo.objects.filter(graduationYear=(senior_year + 2)).prefetch_related('user')
	freshmen = UserInfo.objects.filter(graduationYear=(senior_year + 3)).prefetch_related('user')

	context = RequestContext(request, {
		#'sage': sage,
		#'second': second,
		#'third': third,
		#'fourth': fourth,
		#'first': first,
		#'herald': herald,
		'seniors': seniors,
		'juniors': juniors,
		'sophomores': sophomores,
		'freshmen': freshmen
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