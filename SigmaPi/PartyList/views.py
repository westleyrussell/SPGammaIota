from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from PartyList.models import Party, PartyGuest, PartyJob, AddMaleGuestForm
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime

@login_required
def parties(request):
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

	if request.method == 'POST': # If the form has been submitted...
		form = AddMaleGuestForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			name = form.cleaned_data['name']
			g = Guest(name=name, birthDate=datetime.now(), gender="Male")
			g.save()
			return HttpResponseRedirect('/secure/parties/' + party + '/guests') # Redirect after POST
	else:
		form = AddMaleGuestForm() # An unbound form


	requested_party = Party.objects.get(name__exact=party)
	partyguests = PartyGuest.objects.filter(party=requested_party)
	context = RequestContext(request, {
			'partyname': party,
			'partyguests': partyguests,
			'form': form,
			'redirect': '/secure/parties/' + party + '/guests'
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
			'partyname': party,
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