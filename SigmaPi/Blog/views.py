from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from datetime import datetime

from Blog.models import BlogPost, BlogPostForm


def index(request):
	"""get an ordered (by date) list of all blog posts to deliver to the client.
	consider preforming more filtering here"""

	all_posts = BlogPost.objects.order_by('-date')

	context = RequestContext(request,{
		'highlighted_posts': all_posts,
		'recent_posts': all_posts,
	})
	return render(request,'index.html',context)


def blog_post(request, slug):
	""" View for a single blog post """
	post = BlogPost.objects.filter(path=slug)[0]

	context = RequestContext(request, {
		'post': post,
		})

	return render(request, 'blog.html', context)

@permission_required('Blog.change_blogpost', login_url='PubSite.views.permission_denied')
def secure_index(request):

	posts = BlogPost.objects.order_by("-date")

	context = RequestContext(request, {
		'posts': posts,
		})

	return render(request, 'secure/blog_index.html', context);

@permission_required('Blog.change_blogpost', login_url='PubSite.views.permission_denied')
def edit_blog(request, slug):
	""" View for editing a blog post """

	post = BlogPost.objects.filter(path=slug)[0]

	# Find the existing post.
	if request.method == 'POST':
		form = BlogPostForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			form.save();
			return redirect('Blog.views.secure_index')
	
	form = BlogPostForm(instance=post)
	context = RequestContext(request, {
		'form': form,
		'post': post,
		})

	return render(request, 'secure/edit_blog.html', context)

@permission_required('Blog.add_blogpost', login_url='PubSite.views.permission_denied')
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

			return redirect('Blog.views.secure_index')
		else:
			context = RequestContext(request, {
				'form':form,
				'error': form.errors
				})

			return render(request, 'secure/add_blog.html', context)

	form = BlogPostForm()
	context = RequestContext(request, {
		'form': form,
		})
	return render(request, 'secure/add_blog.html', context)

@permission_required('Blog.delete_blogpost', login_url='PubSite.views.permission_denied')
def delete_blog(request):
	"""
		Deletes the blog with the id that is sent in the post request
	"""

	if request.method == 'POST':
		blog_id = strip_tags(request.POST['post_id'])

		post = BlogPost.objects.get(pk=blog_id)
		post.delete()

	return redirect('Blog.views.secure_index')




