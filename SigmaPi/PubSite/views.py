from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from PubSite.models import BlogPost

def index(request):
	"""get an ordered (by date) list of all blog posts to deliver to the client.
	consider preforming more filtering here"""

	all_posts = BlogPost.objects.order_by('date')

	context = RequestContext(request,{
		'highlighted_posts': all_posts,
		'recent_posts': all_posts,
	})
	return render(request,'home.html',context)

def blog_index(request):
	return index(request)

def blog_post(request, path):
	""" View for a single blog post """
	return HttpResponse("Single blog post here " + path)

def hisotry(request):
	"""view for the static chapter history page"""
	return render(request,'history.html',None)

def service(request):
	"""view for the static chapter service page"""
	return render(request,'service.html',None)
