from django.core import serializers
from django.http import HttpResponse

from django.template import RequestContext
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required, login_required

from django.utils.html import strip_tags
from django.utils import simplejson, dateformat

from datetime import datetime

from Links.models import Link, Like, Comment, LinkForm, CommentForm

@permission_required('Links.access_link', login_url='PubSite.views.permission_denied')
def view_all(request):
	"""
		Displays all of the links in the system.
	"""
	linkform = LinkForm()
	commentform = CommentForm()

	general_links = Link.objects.filter(promoted=False).order_by('-lastCommented')
	promoted_links = Link.objects.filter(promoted=True).order_by('date')
	liked_links = Like.objects.filter(liker=request.user).values_list('link', flat=True)

	context = RequestContext(request, {
		'linkform':linkform,
		'commentform':commentform,
		'general_links': general_links,
		'promoted_links': promoted_links,
		'links_liked': liked_links,
		})

	return render(request, "secure/links_view_all.html", context)

@permission_required('Links.access_link', login_url='PubSite.views.permission_denied')
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

@permission_required('Links.access_link', login_url='PubSite.views.permission_denied')
def check_for_updates(request):
	"""
		Retrieve all comments posted after a given time.
	"""

	try:
		last_time = datetime.fromtimestamp(float(strip_tags(request.GET['last'])))
		comments = Comment.objects.filter(date__gt=last_time).exclude(commentor=request.user).order_by('date')
		links = Link.objects.all()

		response = {}
		response['comments'] = []

		for comment in comments:
			serialized = {}
			serialized['content'] = comment.comment
			serialized['poster'] = comment.commentor.first_name + " " + comment.commentor.last_name
			serialized['date'] = dateformat.format(comment.date, 'F j, Y, P')
			serialized['pk'] = comment.link.pk
			response['comments'].append(serialized)

		response['links'] = []
		for link in links:
			link_serial = {}
			link_serial['pk'] = link.pk
			link_serial['commentCount'] = link.commentCount
			link_serial['likeCount'] = link.likeCount
			response['links'].append(link_serial)

		return HttpResponse(simplejson.dumps(response), content_type="application/json")
	except Exception, e:
		raise e

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
			link.lastCommented = datetime.now()
			link.lastAccessed = link.lastCommented

			if not request.user.has_perm('Links.promote_link'):
				link.promoted = False
			link.save()

		print(form.errors)

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
			desired_link.lastCommented = comment.date
			desired_link.save()

		response = {}
		response['author'] = request.user.first_name + " " + request.user.last_name
		response['date'] = dateformat.format(comment.date, 'F j, Y, P')
		response['comment'] = comment.comment
		response['commentCount'] = desired_link.commentCount
		return HttpResponse(simplejson.dumps(response), content_type="application/json")
	else:
		return redirect('PubSite.views.permission_denied')

@permission_required('Links.add_like', login_url='PubSite.views.permission_denied')
def change_like(request, link):
	"""
		Adds a like to a given link
	"""
	if request.method == 'POST':

		try:
			desired_link = Link.objects.get(pk=link)
		except Exception, e:
			return redirect('PubSite.views.permission_denied')

		# Check if user has liked on this before.
		try:
			priorLike = Like.objects.get(link=link, liker=request.user)
			priorLike.delete()
			desired_link.likeCount = desired_link.likeCount - 1
			desired_link.save()
		except Exception, e:
			# if a like doesnt exist, just create one.
			like = Like()
			like.liker = request.user
			like.link = desired_link
			like.save()
			desired_link.likeCount = desired_link.likeCount + 1
			desired_link.save()

		response = {}
		response['likes'] = desired_link.like_set.count()
		return HttpResponse(simplejson.dumps(response), content_type="application/json")

	else:
		return redirect('PubSite.views.permission_denied')


