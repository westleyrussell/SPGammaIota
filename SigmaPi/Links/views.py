from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from datetime import datetime
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.http import HttpResponse
from Links.models import Link, Like, Comment, LinkForm, CommentForm

@login_required
def view_all(request):
	"""
		Displays all of the links in the system.
	"""
	linkform = LinkForm()
	commentform = CommentForm()

	links = Link.objects.all()
	liked_links = Like.objects.filter(liker=request.user).values_list('link', flat=True)

	context = RequestContext(request, {
		'linkform':linkform,
		'commentform':commentform,
		'links': links,
		'links_liked': liked_links,
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
			link.likeCount = 0
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

@permission_required('Links.add_like', login_url='PubSite.views.permission_denied')
@csrf_exempt
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
			priorLike = Like.objects.get(link=desired_link, liker=request.user)

			desired_link.likeCount = desired_link.likeCount - 1
			priorLike.delete()
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
		response['likes'] = desired_link.likeCount
		return HttpResponse(simplejson.dumps(response), content_type="application/json")

	else:
		return redirect('PubSite.views.permission_denied')


