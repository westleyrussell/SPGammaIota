from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

def index(request):
	""" View for the index landing page of the site """
	context = RequestContext(request,{
		'motd': 'boatie rules'
	})
	return render(request,'index.html',context)

def blog_index(request):
	""" View for all of the blogs/blog overview """
	return HttpResponse("All blogs here")

def blog_post(request, path):
	""" View for a single blog post """
	return HttpResponse("Single blog post here " + path)

def hisotry(request):
	"""view for the static chapter history page"""
	return render(request,'history.html',None)

def service(request):
	"""view for the static chapter service page"""
	return render(request,'service.html',None)
