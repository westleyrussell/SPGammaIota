from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.utils.html import strip_tags
from django.template.defaultfilters import slugify
from datetime import datetime
from sendfile import sendfile
from Archives.models import Guide, GuideForm, MeetingMinutes, MinutesForm, HouseRules, RulesForm, Bylaws, BylawsForm


@permission_required('Archives.access_guide', login_url='PubSite.views.permission_denied')
def index(request):
	"""
		View for the index page of the archives
	"""
	return guides(request)

@permission_required('Archives.access_bylaws', login_url='PubSite.views.permission_denied')
def bylaws(request):
	"""
		View for all bylaws.
	"""
	form = BylawsForm()

	if request.method == 'POST':
		if request.user.has_perm('Archives.add_bylaws'):
			form = BylawsForm(request.POST, request.FILES)

			if form.is_valid():
				bylaw = form.save(commit=False)
				bylaw.date = datetime.now()
				bylaw.save()
		else:
			redirect('PubSite.views.permission_denied')

	bylaws = Bylaws.objects.all()
	if bylaws:
		latest = bylaws.latest('date')
	else:
		latest = None

	context = RequestContext(request, {
		'latest': latest,
		'bylaws': bylaws,
		'form': form
		})

	return render(request, "secure/archives_bylaws.html", context)

@permission_required('Archives.access_bylaws', login_url='PubSite.views.permission_denied')
def download_bylaw(request, bylaw):
	"""
		View for downloading bylaws
	"""

	bylawObject = Bylaws.objects.get(pk=bylaw)
	return sendfile(request, bylawObject.filepath.path, attachment=True, attachment_filename="Bylaws " + str(bylawObject.date))


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

@permission_required('Archives.access_houserules', login_url='PubSite.views.permission_denied')
def rules(request):
	"""
		View for all house rules
	"""
	form = RulesForm()

	# If its a POST, we're trying to update the rules.
	if request.method == 'POST':
		# Check permissions before going forward
		if request.user.has_perm('Archives.add_houserules'):
			form = RulesForm(request.POST, request.FILES)

			if form.is_valid():
				rule = form.save(commit=False)
				rule.date = datetime.now()
				rule.save()
		else:
			redirect('PubSite.views.permission_denied')

	rules = HouseRules.objects.all()
	if rules:
		latest = rules.latest('date')
	else:
		latest = None

	context = RequestContext(request, {
		'latest': latest,
		'rules': rules,
		'form': form
		})

	return render(request, "secure/archives_rules.html", context)

@permission_required('Archives.access_houserules', login_url='PubSite.views.permission_denied')
def download_rules(request, rules):
	"""
		View for downloading rules
	"""

	houseRuleObject = HouseRules.objects.get(pk=rules)

	return sendfile(request, houseRuleObject.filepath.path, attachment=True, attachment_filename="House Rules " + str(houseRuleObject.date))

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

@permission_required('Archives.access_meetingminutes', login_url='PubSite.views.permission_denied')
def minutes(request):
	"""
		View for all minutes
	"""
	form = MinutesForm()

	# If its a POST, we're trying to add meeting minutes.
	if request.method == 'POST':
		# Check for permissions first.
		if request.user.has_perm('Archives.add_meetingminutes'):
			form = MinutesForm(request.POST, request.FILES)

			if form.is_valid():
				minute = form.save()
				form = MinutesForm()
		else:
			redirect('PubSite.views.permission_denied')


	# Only get the minutes since the user was initiated.
	try:
		user_initiated = request.user.userinfo.pledgeClass.dateInitiated
	except:
		user_initiated = datetime.now()

	minutes = MeetingMinutes.objects.filter(date__gt=user_initiated)
	context = RequestContext(request, {
		'minutes': minutes,
		'form': form,
		})

	return render(request, "secure/archives_minutes.html", context)

@permission_required('Archives.access_meetingminutes', login_url='PubSite.views.permission_denied')
def download_minutes(request, minutes):
	"""
		View for downloading minutes
	"""

	minutesObject = MeetingMinutes.objects.get(pk=minutes)

	try:
		user_initiated = request.user.userinfo.pledgeClass.dateInitiated
	except:
		return redirect('PubSite.views.permission_denied')

	if user_initiated >= minutesObject.date:
		return redirect('PubSite.views.permission_denied')

	return sendfile(request, minutesObject.filepath.path, attachment=True, attachment_filename="Meeting Minutes " + str(minutesObject.date))


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

@permission_required('Archives.access_guide', login_url='PubSite.views.permission_denied')
def guides(request):
	"""
		View for all guides
	"""

	form = GuideForm()

	# If its a POST we're trying to create a guide.
	if request.method == 'POST':
		# Check if user has permission to do so first.
		if request.user.has_perm('Archives.add_guide'):
			form = GuideForm(request.POST, request.FILES)

			if form.is_valid():
				guide = form.save(commit=False)
				guide.path = slugify(guide.name)[:14]
				guide.save()
				form = GuideForm()
		else:
			redirect('PubSite.views.permission_denied')

	guides = Guide.objects.all()
	context = RequestContext(request, {
		'guides': guides,
		'form': form,
		})

	return render(request, "secure/archives_guides.html", context)

@permission_required('Archives.access_meetingminutes', login_url='PubSite.views.permission_denied')
def download_guides(request, guides):
	"""
		View for downloading guides
	"""

	guideObject = Guide.objects.get(pk=guides)

	return sendfile(request, guideObject.filepath.path, attachment=True, attachment_filename=guideObject.name)

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
