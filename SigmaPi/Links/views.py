from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from datetime import datetime
from django.utils.html import strip_tags

from Links.models import Link, Opinion, Comment, LinkForm, CommentForm

@login_required
def view_all(request):
	"""
		Displays all of the links in the system.
	"""
	linkform = LinkForm()
	commentform = CommentForm()

	links = Link.objects.all()

	context = RequestContext(request, {
		'linkform':linkform,
		'commentform':commentform,
		'links': links,
		})

	return render(request, "secure/links_view_all.html", context)

@login_required
def visit_link(request, link):
	"""
		Records a visit to the given link and redirects the user to it.
	"""
	
	try:
		desired_link = Link.objects.get(pk=link)
		desired_link.lastAccessed = datetime.now()
		desired_link.timesAccessed = desired_link.timesAccessed + 1
		desired_link.save()
		return redirect(desired_link.url)
	except Exception, e:
		return redirect('PubSite.views.permission_denied')


@permission_required('Links.add_link', login_url='PubSite.views.permission_denied')
def add_link(request):
	"""
		Creates a new link to add to the system
	"""
	if request.method == 'POST':
		form = LinkForm(request.POST)

		if form.is_valid():
			link = form.save(commit=False)
			link.poster = request.user
			link.date = datetime.now()
			link.timesAccessed = 0
			link.lastAccessed = datetime.now()
			link.piValue = 0
			link.commentCount = 0
			link.promoted = False
			link.save()

		return redirect('Links.views.view_all')
	else:
		return redirect('PubSite.views.permission_denied')

@permission_required('Links.add_comment', login_url='PubSite.views.permission_denied')
def add_comment(request, link):
	"""
		Creates a new comment to a given link.
	"""

	try:
		desired_link = Link.objects.get(pk=link)
	except Exception, e:
		return redirect('PubSite.views.permission_denied')


	if request.method == 'POST':
		form = CommentForm(request.POST)

		if form.is_valid():
			comment = form.save(commit=False)
			comment.commentor = request.user
			comment.date = datetime.now()
			comment.link = desired_link
			comment.save()
			desired_link.commentCount = desired_link.commentCount + 1
			desired_link.save()

		return redirect('Links.views.view_all')
	else:
		return redirect('PubSite.views.permission_denied')

@permission_required('Links.add_opinion', login_url='PubSite.views.permission_denied')
def change_opinion(request, link):
	"""
		Adds an PiOpinion to a given link
	"""
	if request.method == 'POST':

		try:
			desired_link = Link.objects.get(pk=link)
			op_id = strip_tags(request.POST['opin_id'])
		except Exception, e:
			return redirect('PubSite.views.permission_denied')

		if op_id == 'P':
			positive = True
			pival = 1
		else:
			positive = False
			pival = -1

		# Check if user has opinionated on this before.
		try:
			priorOpinion = Opinion.objects.get(link=desired_link, opinionator=request.user)

			# If we pressed the same button as before, just remove the opinion completely.
			if priorOpinion.positiveOpinion == positive:
				desired_link.piValue = desired_link.piValue + pival
				priorOpinion.delete()
			else:
				# if we pressed the opposite button, add 2 * its value to negate the old opinion and add a new one.
				desired_link.piValue = desired_link.piValue + (2 * pival)
				priorOpinion.positiveOpinion = positive
				priorOpinion.save()
				desired_link.save()
		except Exception, e:
			# if an opinion doesnt exist, just create one.
			opinion = Opinion()
			opinion.opinionator = request.user
			opinion.link = desired_link
			opinion.positiveOpinion = positive
			opinion.save()
			desired_link.piValue = desired_link.piValue + pival
			desired_link.save()

		return redirect('Links.views.view_all')
	else:
		return redirect('PubSite.views.permission_denied')


