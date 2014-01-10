from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.utils.html import strip_tags

from Archives.models import Guide, MeetingMinutes, HouseRules, Bylaws


@login_required
def index(request):
	"""
		View for the index page of the archives
	"""
	return guides(request)#render(request, "secure/archives_index.html", None)

@login_required
def bylaws(request):
	"""
		View for all bylaws.
	"""
	bylaws = Bylaws.objects.all()
	context = RequestContext(request, {
		'bylaws': bylaws,
		})

	return render(request, "secure/archives_bylaws.html", context)

@permission_required('Archives.delete_bylaws', login_url='PubSite.views.permission_denied')
def delete_bylaw(request):
	"""
		Deletes the bylaws with the given primary key.
	"""

	if request.method == 'POST':
		bylaw_id = strip_tags(request.POST['post_id'])

		post = Bylaws.objects.get(pk=bylaw_id)
		post.delete()
	return redirect('Archives.views.bylaws')

@permission_required('Archives.add_bylaws', login_url='PubSite.views.permission_denied')
def create_bylaw(request):
	pass

@login_required
def rules(request):
	"""
		View for all house rules
	"""

	rules = HouseRules.objects.all()
	context = RequestContext(request, {
		'rules': rules,
		})

	return render(request, "secure/archives_rules.html", context)

@permission_required('Archives.delete_houserules', login_url='PubSite.views.permission_denied')
def delete_rules(request):
	"""
		Deletes the rules with the given primary key.
	"""

	if request.method == 'POST':
		rules_id = strip_tags(request.POST['post_id'])

		post = HouseRules.objects.get(pk=rules_id)
		post.delete()
	return redirect('Archives.views.rules')

@permission_required('Archives.add_houserules', login_url='PubSite.views.permission_denied')
def create_rules(request):
	pass

@login_required
def minutes(request):
	"""
		View for all minutes
	"""

	minutes = MeetingMinutes.objects.all()
	context = RequestContext(request, {
		'minutes': minutes,
		})

	return render(request, "secure/archives_minutes.html", context)

@permission_required('Archives.delete_meetingminutes', login_url='PubSite.views.permission_denied')
def delete_minutes(request):
	"""
		Deletes the minutes with the given primary key.
	"""

	if request.method == 'POST':
		minutes_id = strip_tags(request.POST['post_id'])

		post = MeetingMinutes.objects.get(pk=minutes_id)
		post.delete()
	return redirect('Archives.views.minutes')

@permission_required('Archives.add_meetingminutes', login_url='PubSite.views.permission_denied')
def create_minutes(request):
	pass

@login_required
def guides(request):
	"""
		View for all guides
	"""

	guides = Guide.objects.all()
	context = RequestContext(request, {
		'guides': guides,
		})

	return render(request, "secure/archives_guides.html", context)

@permission_required('Archives.delete_guide', login_url='PubSite.views.permission_denied')
def delete_guide(request):
	"""
		Deletes the guide with the given primary key.
	"""

	if request.method == 'POST':
		guide_id = strip_tags(request.POST['post_id'])

		post = Guide.objects.get(pk=guide_id)
		post.delete()
	return redirect('Archives.views.guides')

@permission_required('Archives.add_guide', login_url='PubSite.views.permission_denied')
def create_guide(request):
	pass