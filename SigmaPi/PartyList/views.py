from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from PartyList.models import Party, PartyGuest, PartyJob
from django.http import HttpResponse
from django.template import RequestContext

#View for all parties
@login_required
def parties(request):
	parties = Party.objects.all()
	context = RequestContext(request, {
		'all_parties': parties,
		})
	return render(request, 'parties.html', context)

#View for all guests on the list for a party
@login_required
def guests(request, party):
	requested_party = Party.objects.get(name__exact=party)
	partyguests = PartyGuest.objects.filter(party=requested_party)
	context = RequestContext(request, {
			'partyname': party,
			'partyguests': partyguests
		})
	return render(request, 'partyguests.html', context)

#View for all jobs for a party
@login_required
def jobs(request, party):
	requested_party = Party.objects.get(name__exact=party)
	partyjobs = PartyJob.objects.filter(party=requested_party)
	context = RequestContext(request, {
			'partyname': party,
			'partyjobs': partyjobs
		})
	return render(request, 'partyjobs.html', context)