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
import csv

def userCanEdit(user=None,pg=None):
	"""return true if the given user can edit the party guest making this function 
	allows us to add more cases in which a type of user can edit a guest"""
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
			return error('guest already on list',code=501)
	else:
		form = GuestForm(request.POST)
		if form.is_valid():
			guest = form.save()
		else:
			return error('invalid guest paramaters or format',code=502)

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
def updateCount(request,party):
	"""adjust the guest count for a given party and gender"""

	party = Party.objects.get(name__exact=party)
	try:
		gender = request.POST.get('gender')
		delta = int(request.POST.get('delta'))
	except:
		return error('erroneous gender or delta parameters in POST request')
	if gender == 'guys':
		party.guycount+=delta
	elif gender == 'girls':
		party.girlcount+=delta
	else:
		return error('improper gender parameter')

	party.save()
	return success('count updated successfully')

@login_required
@csrf_exempt
def signin(request,party,id):
	"""signin a guest with given id"""
	try:
		party = Party.objects.get(name__exact=party)
		g,pg = getFullGuest(party,id)
		pg.signedIn = True
		pg.save()
	except:
		return error('issue signing in guest')

	return success('fine')

@login_required
@csrf_exempt
def signout(request,party,id):
	"""signin a guest with given id"""
	try:
		party = Party.objects.get(name__exact=party)
		g,pg = getFullGuest(party,id)
		pg.signedIn = False
		pg.save()
	except:
		return error('issue signing out guest')

	return success('fine')



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
def export_list(request,party):
	"""export the guest list as a csv file. This uses the native csv module
	that comes bundled with python. Using excel would require a 3rd party 
	module, and hardly provides benefits over a standard csv format"""

	requested_party = Party.objects.get(name__exact=party)
	partyguests = PartyGuest.objects.filter(party=requested_party).order_by('guest__name')

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="guests.csv"'

	writer = csv.writer(response)
	writer.writerow(['Name','Added By'])

	for pg in partyguests:
		writer.writerow([pg.guest.name,pg.addedBy])

	return response


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
	response['guests'] = [guest.toJSON() for guest in guests]
	response['gcount'] = len(guests)

	return HttpResponse(json.dumps(response), content_type="application/json")