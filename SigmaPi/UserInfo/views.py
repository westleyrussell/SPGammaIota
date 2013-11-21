from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext

from UserInfo import utils
from UserInfo.models import UserInfo


def users(request):
	"""
		Provides the collections of brothers in the house.
		Organizes them based on year and exec positions.
	"""

	# Find out what current year is the senior year grad date.
	senior_year = utils.get_senior_year()

	# get the execs
	try:
		sage = User.objects.get(groups__name='Sage')
	except:
		sage = None
	try:
		second = User.objects.get(groups__name='2nd Counselor')
	except:
		second = None
	try:
		third = User.objects.get(groups__name='3rd Counselor')
	except:
		third = None
	try:
		fourth = User.objects.get(groups__name='4th Counselor')
	except:
		fourth = None
	try:
		first = User.objects.get(groups__name='1st Counselor')
	except:
		first = None
	try:
		herald = User.objects.get(groups__name='Herald')
	except:
		herald = None

	# Get the rest of the users.  Exclude pledges or any execs.
	seniors = User.objects.filter(userinfo__graduationYear=senior_year).prefetch_related('userinfo')
	seniors = seniors.exclude(groups__name='Pledges')
	seniors = seniors.exclude(groups__name='Alumni')

	juniors = User.objects.filter(userinfo__graduationYear=(senior_year + 1)).prefetch_related('userinfo')
	juniors = juniors.exclude(groups__name='Pledges')
	juniors = juniors.exclude(groups__name='Alumni')

	sophomores = User.objects.filter(userinfo__graduationYear=(senior_year + 2)).prefetch_related('userinfo') 
	sophomores = sophomores.exclude(groups__name='Pledges')
	sophomores = sophomores.exclude(groups__name='Alumni')

	freshmen = User.objects.filter(userinfo__graduationYear=(senior_year + 3)).prefetch_related('userinfo')
	freshmen = freshmen.exclude(groups__name='Pledges')
	freshmen = freshmen.exclude(groups__name='Alumni')

	# Exclude the execs, if applicable.
	if sage is not None:
		seniors = seniors.exclude(username=sage.username)
		juniors = juniors.exclude(username=sage.username)
		sophomores = sophomores.exclude(username=sage.username)
		freshmen = freshmen.exclude(username=sage.username)

	if second is not None:
		seniors = seniors.exclude(username=second.username)
		juniors = juniors.exclude(username=second.username)
		sophomores = sophomores.exclude(username=second.username)
		freshmen = freshmen.exclude(username=second.username)

	if third is not None:
		seniors = seniors.exclude(username=third.username)
		juniors = juniors.exclude(username=third.username)
		sophomores = sophomores.exclude(username=third.username)
		freshmen = freshmen.exclude(username=third.username)

	if fourth is not None:
		seniors = seniors.exclude(username=fourth.username)
		juniors = juniors.exclude(username=fourth.username)
		sophomores = sophomores.exclude(username=fourth.username)
		freshmen = freshmen.exclude(username=fourth.username)

	if first is not None:
		seniors = seniors.exclude(username=first.username)
		juniors = juniors.exclude(username=first.username)
		sophomores = sophomores.exclude(username=first.username)
		freshmen = freshmen.exclude(username=first.username)

	if herald is not None:
		seniors = seniors.exclude(username=herald.username)
		juniors = juniors.exclude(username=herald.username)
		sophomores = sophomores.exclude(username=herald.username)
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