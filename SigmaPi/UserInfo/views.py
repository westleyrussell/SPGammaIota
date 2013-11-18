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
	sage = User.objects.get(groups__name='Sage')
	second = User.objects.get(groups__name='2nd Counselor')
	third = User.objects.get(groups__name='3rd Counselor')
	fourth = User.objects.get(groups__name='4th Counselor')
	first = User.objects.get(groups__name='1st Counselor')
	herald = User.objects.get(groups__name='Herald')

	# get the rest
	seniors = User.objects.filter(userinfo__graduationYear=senior_year).prefetch_related('userinfo')
	seniors = seniors.exclude(groups__name='Pledges')
	seniors = seniors.exclude(groups__name='Alumni')
	seniors = seniors.exclude(username=sage.username)
	seniors = seniors.exclude(username=second.username)
	seniors = seniors.exclude(username=third.username)
	seniors = seniors.exclude(username=fourth.username)
	seniors = seniors.exclude(username=first.username)
	seniors = seniors.exclude(username=herald.username)

	juniors = User.objects.filter(userinfo__graduationYear=(senior_year + 1)).prefetch_related('userinfo')
	juniors = juniors.exclude(groups__name='Pledges')
	juniors = juniors.exclude(groups__name='Alumni')
	juniors = juniors.exclude(username=sage.username)
	juniors = juniors.exclude(username=second.username)
	juniors = juniors.exclude(username=third.username)
	juniors = juniors.exclude(username=fourth.username)
	juniors = juniors.exclude(username=first.username)
	juniors = juniors.exclude(username=herald.username)

	sophomores = User.objects.filter(userinfo__graduationYear=(senior_year + 2)).prefetch_related('userinfo') 
	sophomores = sophomores.exclude(groups__name='Pledges')
	sophomores = sophomores.exclude(groups__name='Alumni')
	sophomores = sophomores.exclude(username=sage.username)
	sophomores = sophomores.exclude(username=second.username)
	sophomores = sophomores.exclude(username=third.username)
	sophomores = sophomores.exclude(username=fourth.username)
	sophomores = sophomores.exclude(username=first.username)
	sophomores = sophomores.exclude(username=herald.username)

	freshmen = User.objects.filter(userinfo__graduationYear=(senior_year + 3)).prefetch_related('userinfo')
	freshmen = freshmen.exclude(groups__name='Pledges')
	freshmen = freshmen.exclude(groups__name='Alumni')
	freshmen = freshmen.exclude(username=sage.username)
	freshmen = freshmen.exclude(username=second.username)
	freshmen = freshmen.exclude(username=third.username)
	freshmen = freshmen.exclude(username=fourth.username)
	freshmen = freshmen.exclude(username=first.username)
	freshmen = freshmen.exclude(username=herald.username)

	context = RequestContext(request, {
		'sage': sage,
		'second': second,
		'third': third,
		'fourth': fourth,
		'first': first,
		'herald': herald,
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