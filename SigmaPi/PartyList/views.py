from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
from PartyList.models import Party, PartyGuest, PartyJob, AddMaleGuestForm
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.utils import simplejson
from PartyList.widgets import GuestForm, PartyForm, EditPartyInfoForm, List
from django.utils.html import strip_tags
import dateutil.parser


@login_required
def index(request):
	"""
		View for all parties
	"""

	parties = Party.objects.all()
	context = RequestContext(request, {
		'all_parties': parties,
	})
	return render(request, 'parties.html', context)

@login_required
def guests(request, party):
	"""
		View for all guests on the list for a party
	"""
	requested_party = Party.objects.get(name__exact=party)
	partyguests = PartyGuest.objects.filter(party=requested_party).order_by('guest__name')
	guys = List('guys')
	girls = List('girls')
	for pg in partyguests:
		if pg.guest.gender == 'M':
			guys.guests.append(pg)
		else:
			girls.guests.append(pg)

	partymode = False
	closedate = requested_party.date
	closedatetime = datetime(closedate.year, closedate.month, closedate.day, 20)

	if closedatetime < datetime.now():
		guys.signed_in = requested_party.guycount
		girls.signed_in = requested_party.girlcount
		partymode = True

	context = RequestContext(request, {
			'partyname': requested_party.displayname,
			'partymode': partymode,
			'lists': [guys,girls],
			'redirect': '/secure/parties/' + party + '/guests',
		})
	return render(request, 'partyguests.html', context)

@login_required
def jobs(request, party):
	"""
		View for all jobs for a party
	"""

	requested_party = Party.objects.get(name__exact=party)
	partyjobs = PartyJob.objects.filter(party=requested_party)
	context = RequestContext(request, {
			'partyname': requested_party.displayname,
			'partyjobs': partyjobs
		})
	return render(request, 'partyjobs.html', context)

@permission_required('PartyList.manage_parties', login_url='Secure.views.home')
@login_required
def add_party(request):
	"""
		Provides a view to add a party.
	"""
	context = RequestContext(request, {
		'message': []
		})

	if request.method == 'POST':
		form = PartyForm(request.POST)
		if form.is_valid():
			partyname = strip_tags(request.POST['name']).replace(" ","_")
			partydate = strip_tags(request.POST['date'])
			exists = Party.objects.filter(name=partyname, date=partydate).count()
			if exists:
				context['message'].append("A party with this name and date already exists.")
			else:
				party = form.save()
				context['message'].append(party.displayname() + " successfully added.")
		else:
			context['message'].append("Error adding party.")
	return render(request, 'add_party.html', context)

@permission_required('PartyList.manage_parties', login_url='Secure.views.home')
@login_required
def manage_parties(request):
	"""
		Provides a view to manage all of the parties in the system.
	"""

	all_parties = Party.objects.all().order_by("date")

	context = RequestContext(request, {
		'all_parties': all_parties,
		})

	return render(request, 'manage_parties.html', context)

@permission_required('PartyList.manage_parties', login_url='Secure.views.home')
@login_required
def edit_party(request, party, date):
	"""
		Provides a view to edit a single party.
	"""
	requested_party = Party.objects.get(name__exact=party, date__exact=date)

	if request.method == 'POST':
		form = EditPartyInfoForm(request.POST, instance=requested_party)
		if form.is_valid():
			partyname = strip_tags(request.POST['name']).replace(" ","_")
			partydate = strip_tags(request.POST['date'])
			exists = Party.objects.filter(name=partyname, date=partydate).count()
			if exists:
				return redirect("PartyList.views.manage_parties")
			else:
				form.save()
				return redirect("PartyList.views.manage_parties")
	else:
		form = EditPartyInfoForm(instance=requested_party)
	


	context = RequestContext(request, {
		'requested_party': requested_party,
		'form': form,
		'error': form.errors
		})

	return render(request, 'edit_party.html', context)

@permission_required('PartyList.manage_parties', login_url='Secure.views.home')
@login_required
def delete_party(request, party, date):
	"""
		Deletes the party with the name that is sent in the post request
	"""

	party = Party.objects.get(name=party, date=date)
	party.delete()
	return redirect("PartyList.views.manage_parties")
