from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from PubSite.models import BlogPost

# View for the index landing page of the site
def index(request):
	context = RequestContext(request,{
		'motd': 'calder rules'
	})
	return render(request,'index.html',context)

# Provides a view for all blog posts
def blog_index(request):
	"""get an ordered (by date) list of all blog posts to deliver to the client.
	consider preforming more filtering here"""
	all_posts = BlogPost.objects.order_by('date')
	context = RequestContext(request,{
		'posts' : all_posts
	})
	return render(request,'index.html',context)

# View for an individual blog post
def blog_post(request, path):
	return HttpResponse("Single blog post here " + path)

def hisotry(request):
	"""view for the static chapter history page"""
	return render(request,'history.html',None)

def service(request):
	"""view for the static chapter service page"""
	return render(request,'service.html',None)
