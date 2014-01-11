from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from datetime import datetime

from Links.models import Link, Opinion, Comment, LinkForm

@login_required
def view_all(request):
	"""
		Displays all of the links in the system.
	"""
	return render(request, "secure/links_view_all.html", None)

@login_required
def visit_link(request, link):
	"""
		Records a visit to the given link and redirects the user to it.
	"""
	pass

@login_required
def add_link(request):
	"""
		Creates a new link to add to the system
	"""
	pass

@login_required
def add_comment(request, link):
	"""
		Creates a new comment to a given link.
	"""
	pass

@login_required
def change_opinion(request, link):
	"""
		Adds an PiOpinion to a given link
	"""
	pass


