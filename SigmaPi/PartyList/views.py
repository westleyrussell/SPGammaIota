from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from PartyList.models import Party, PartyGuest, PartyJob, AddMaleGuestForm
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.utils import simplejson
from PartyList.widgets import GuestForm, List


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
	print type(party)
	requested_party = Party.objects.get(name__exact=party)
	partyguests = PartyGuest.objects.filter(party=requested_party)
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
		partymode = True

	partymode = False
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

def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'guests.html', {
        'form': form,
    })


