from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

# View for the index landing page of the site
def index(request):
	context = RequestContext(request,{
		'motd': 'calder rules'
	})
	return render(request,'index.html',context)

# Provides a view for all blog posts
def blog_index(request):
	return HttpResponse("All blogs here")

# View for an individual blog post
def blog_post(request, path):
	return HttpResponse("Single blog post here " + path)

def hisotry(request):
	"""view for the static chapter history page"""
	return render(request,'history.html',None)

