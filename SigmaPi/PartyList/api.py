from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from PartyList.models import Party, Guest, PartyGuest, PartyJob
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from PartyList.widgets import GuestForm

import json

def userCanEdit(user=None,pg=None):
	"""return true if the given user can edit the party guest making this function 
	allows us to add more cases in which a type of user can edit a guest"""
	print pg.addedBy, user
	if pg.addedBy == user:
		return True

	return False

def error(message="",code=400):
	"""return an http response with the given error code (400 by default) and message"""
	return HttpResponse(message, status=code)

def success(message="",code=200):
	"""return an http response that simply tells the client their action was successful"""
	return HttpResponse(message,status=code)

def getFullGuest(party,id):
	"""get a guest and its associated partyGuest model, return as a tuple"""
	guest = Guest.objects.get(id=id)
	party = Party.objects.get(name__exact=party)
	pGuest = PartyGuest.objects.get(party=party,guest=guest)

	return guest,pGuest

@login_required
@csrf_exempt
def create(request,party):
	"""create a guest object as well as a partyguest object for the given party"""
	
	# see if the guest already exists
	guest = None
	try:
		guest = Guest.objects.get(name__exact=request.POST.get('name'))
	except:
		pass

	if guest:
		partyguest = PartyGuest.objects.filter(party__exact=Party.objects.get(name__exact=party), guest__exact=guest)
		if partyguest: # if this guest is already on the list for this party
			return error('guest already on list',code=500)
	else:
		form = GuestForm(request.POST)
		if form.is_valid():
			guest = form.save()
		else:
			return error('invalid guest paramaters or format',code=500)

	pGuest = PartyGuest(party=Party.objects.get(name__exact=party), guest=guest, addedBy=request.user)
	pGuest.save()
	return HttpResponse(guest.id,status=200)


@login_required
@csrf_exempt
def update(request,party,id):
	"""update a guest (keyd by the supplied id) for the value provided"""
	try:
		guest,pg = getFullGuest(party,int(id))
	except:
		return error('guest does not exist')

	if userCanEdit(user=request.user,pg=pg):
		form = GuestForm(request.POST,instance=guest)
		if form.is_valid():
			form.save()
			return success()
		else:
			return error('invalid form returned')
	else:
		return error('not allowed to edit guest',code=504)



@login_required
@csrf_exempt
def destroy(request,party,id):
	"""delete a guest (keyd by the supplied id), so long as the current user has domain over them"""
	try:
		guest,pg = getFullGuest(party,int(id))
	except:
		return error('guest does not exist')

	if userCanEdit(user=request.user,pg=pg):
		pg.delete()
		return success()
	else:
		return error('not allowed to delete guest',code=504)


@login_required
@csrf_exempt
def poll(request,party):
	"""
	called by the client to check for guests added after a given time. 
	This allows each clients guest list to be updated in partial real time

		Checks the guests object for new guests added 
		after a supplied time (unix format) and sends
		a json object of those guests back
	"""
	last_stamp = float(request.GET.get('last'))
	last = datetime.fromtimestamp(last_stamp/1000.0) #js timestamp is in milliseconds, time_t is in seconds.
	
	guests = list(PartyGuest.objects.filter(createdAt__gte=last))
	response = {}
	response['guests'] = serializers.serialize('json',guests)
	response['gcount'] = len(guests)

	return HttpResponse(json.dumps(response), content_type="application/json")