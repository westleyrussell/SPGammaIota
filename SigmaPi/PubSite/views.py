from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.template.defaultfilters import slugify

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from datetime import datetime

from PubSite.models import BlogPost, BlogPostForm



def index(request):
	"""get an ordered (by date) list of all blog posts to deliver to the client.
	consider preforming more filtering here"""

	all_posts = BlogPost.objects.order_by('-date')

	context = RequestContext(request,{
		'highlighted_posts': all_posts,
		'recent_posts': all_posts,
	})
	return render(request,'index.html',context)

def blog_index(request):
	return index(request)

def blog_post(request, slug):
	""" View for a single blog post """
	post = BlogPost.objects.filter(path=slug)[0]

	context = RequestContext(request, {
		'post': post,
		})

	return render(request, 'blog.html', context)

@login_required
def edit_blog(request, slug):
	""" View for editing a blog post """

	post = BlogPost.objects.filter(path=slug)[0]

	# Find the existing post.
	if request.method == 'POST':
		form = BlogPostForm(request.POST, instance=post)
		if form.is_valid():
			form.save();
			return redirect('PubSite.views.blog_post', post.path)
	
	form = BlogPostForm(instance=post)
	context = RequestContext(request, {
		'form': form,
		'post': post,
		})

	return render(request, 'edit_blog.html', context)

@login_required
def add_blog(request):
	"""
		Adds a new blog post to the server
	"""
	# Check if the form was submitted.
	if request.method == 'POST':
		form = BlogPostForm(request.POST, request.FILES)

		# Check for form validity.
		if form.is_valid():
			blogpost = form.save(commit=False)

			blogpost.poster = request.user
			blogpost.path = slugify(blogpost.title)
			blogpost.date = datetime.now()
			blogpost.save()

		else:
			context = RequestContext(request, {
				'form':form,
				'error': form.errors
				})

			return render(request, 'add_blog.html', context)

	form = BlogPostForm()
	context = RequestContext(request, {
		'form': form,
		})
	return render(request, 'add_blog.html', context)

def history(request):
	"""view for the static chapter history page"""
	return render(request,'history.html',None)

def service(request):
	"""view for the static chapter service page"""
	return render(request,'service.html',None)
