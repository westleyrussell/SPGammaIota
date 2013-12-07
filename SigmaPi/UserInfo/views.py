from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required, login_required

from UserInfo import utils
from UserInfo.models import UserInfo, EditUserInfoForm


def users(request):
	"""
		Provides the collections of brothers in the house.
		Organizes them based on year and exec positions.
	"""

	# Find out what current year is the senior year grad date.
	senior_year = utils.get_senior_year()

	# Get the execs.  Use try/catch to avoid crashing the site if an exec is missing.
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
	"""
		Provides the view for a single requested user.
	"""


	requested_user = User.objects.get(username__exact=user)
	context = RequestContext(request, {
			'requested_username': user,
			'requested_user': requested_user
		})
	return render(request, 'user.html', context)


def profile(request):
	"""
		Provides a view for the profile of a logged in user.
	"""
	
	if request.user.is_active:
		return single_user(request, request.user.username)
	else:
		return HttpResponse("Not Authenticated")

@permission_required('UserInfo.manage_users', login_url='Secure.views.home')
def add_users(request):
	"""
		Provides a view for the profile of a logged in user.
	"""

	if request.method == 'POST':

		return redirect("UserInfo.views.manage_users")

	return render(request, 'secure/add_users.html', None)

@permission_required('UserInfo.manage_users', login_url='Secure.views.home')
def manage_users(request):
	"""
		Provides a view to manage all of the users in the system.
	"""

	all_users = User.objects.all().order_by("last_name")

	context = RequestContext(request, {
		'all_users': all_users,
		})

	return render(request, 'secure/manage_users.html', context)

@login_required
def edit_user(request, user):
	"""
		Provides a view to edit a single user.
	"""
	requested_user = User.objects.get(username__exact=user)
	if (not requested_user == request.user) and not request.user.is_staff:
		return redirect('PubSite.views.permission_denied')

	if request.method == 'POST':
		form = EditUserInfoForm(request.POST, instance=requested_user.userinfo)
		if form.is_valid():
			form.save()
			return redirect("UserInfo.views.manage_users")
	else:
		form = EditUserInfoForm(instance=requested_user.userinfo)
	


	context = RequestContext(request, {
		'requested_user': requested_user,
		'form': form,
		'error': form.errors
		})

	return render(request, 'secure/edit_user.html', context)

