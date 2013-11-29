from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from PartyList.models import Party, Guest, PartyGuest, PartyJob
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

def error(message,code=400):
	"""return an http response with the given error code (400 by default) and message"""
	return HttpResponse(message, status=code)

@login_required
@csrf_exempt
def create(request,party):
	"""create a guest object as well as a partyguest object for the given party"""
	try:
		name = request.POST.get('name')
		gender = request.POST.get('gender')
	except:
		error('Client did not provide required fields')

	guest = Guest(name=name, gender=gender,birthDate=datetime.now())
	guest.save()

	party = Party.objects.get(name__exact=party)
	pGuest = PartyGuest(party=party, guest=guest,addedBy=request.user)
	pGuest.save()

	return HttpResponse(guest.id,status=200)

@login_required
def update(request,party):
	pass

@login_required
def destroy(request,party):
	pass

@login_required
def poll(request,party):
	"""
	called by the client to check for guests added after a given time. 
	This allows each clients guest list to be updated in partial real time

		Checks the guests object for new guests added 
		after a supplied time (unix format) and sends
		a json object of those guests back
	"""
	last_stamp = request.GET.get('last')
	last = datetime.fromtimestamp(last_stamp)
	
	guests = PartyGuest.objects.filter(createdAt__gte=last)
	response = {}
	response['guests'] = list(guets)

	return HttpResponse(simplejson.dumps(response), content_type="application/json")