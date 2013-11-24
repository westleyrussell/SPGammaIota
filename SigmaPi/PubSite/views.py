from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from PubSite.models import BlogPost

<<<<<<< HEAD
def home(request):
	""" View for the index landing page of the site """
	context = RequestContext(request,{
		'motd': 'boatie rules'
	})
	return render(request,'home.html',context)

def blog_index(request):
=======
def index(request):
>>>>>>> a08f5e851334bf8087cc6c08b10dbeaaa3b7f070
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
