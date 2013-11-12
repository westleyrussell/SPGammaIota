# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#View for the index page
@login_required
def index(request):
	return HttpResponse("Hello World")

#View for all bylaws
@login_required
def bylaws(request):
	return HttpResponse("Bylaws")

#View for a single bylaw
@login_required
def single_bylaw(request, year, month, day):
	return HttpResponse("Bylaws " + year + month + day)

#View for all rules
@login_required
def rules(request):
	return HttpResponse("House Rules")

#View for a single rule
@login_required
def single_rule(request, path):
	return HttpResponse("Rule " + path)

#View for all minutes
@login_required
def minutes(request):
	return HttpResponse("Meeting Minutes")

#View for a single set of minutes
@login_required
def single_minutes(request, year, month, day):
	return HttpResponse("Minutes " + year + month + day)

#View for all guides
@login_required
def guides(request):
	return HttpResponse("Guides")

#View for a single guide
@login_required
def single_guide(request, path):
	return HttpResponse("Guide " + path)

