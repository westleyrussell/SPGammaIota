from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def index(request):
	"""
		View for the index page of the archives
	"""
	return render(request, "secure/archives_index.html", None)

@login_required
def bylaws(request):
	"""
		View for all bylaws.
	"""
	return render(request, "secure/archives_bylaws.html", None)

@login_required
def single_bylaw(request, year, month, day):
	"""
		View for a single bylaw
	"""
	return HttpResponse("Bylaws " + year + month + day)

@login_required
def rules(request):
	"""
		View for all house rules
	"""
	return render(request, "secure/archives_rules.html", None)

@login_required
def single_rule(request, path):
	"""
		View for a single house rule
	"""
	return HttpResponse("Rule " + path)

@login_required
def minutes(request):
	"""
		View for all minutes
	"""
	return render(request, "secure/archives_minutes.html", None)

@login_required
def single_minutes(request, year, month, day):
	"""
		View for a single minutes
	"""
	return HttpResponse("Minutes " + year + month + day)

@login_required
def guides(request):
	"""
		View for all guides
	"""
	return render(request, "secure/archives_guides.html", None)

@login_required
def single_guide(request, path):
	"""
		View for a single guide
	"""
	return HttpResponse("Guide " + path)

