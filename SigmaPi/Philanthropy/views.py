from django.template import RequestContext
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.utils.html import strip_tags
from django.utils import simplejson, dateformat

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User

from datetime import datetime

from Philanthropy.models import HoursRecord, HoursRequest, HoursChangeRecord, HoursRequestForm, HoursAddBrotherForm

@login_required
def index(request):
	"""
		Displays the homepage of the philanthropy module.
	"""
	
	hours_records = HoursRecord.objects.all().exclude(brother__groups__name='Alumni').order_by('-hours')
	
	own_hours = HoursRecord.objects.filter(brother=request.user)

	if own_hours.count() == 0:
		# If we don't have a record, create one.
		record = HoursRecord()
		record.hours = 0
		record.brother = request.user
		record.save()
		own_hours = record
	else:
		own_hours = own_hours[0]

	hours_form = HoursRequestForm()

	context = RequestContext(request, {
	'own_hours': own_hours,
	'hours_records': hours_records,
	'hours_form': hours_form,
	})

	return render(request, "secure/philanthropy_index.html", context)

@permission_required('Philanthropy.add_hoursrequest', login_url='PubSite.views.permission_denied')
def request_hours(request):
	"""
		Registers an hours request to be reviewed by the phianthropy chairman
	"""
	if request.method == 'POST':
		form = HoursRequestForm(request.POST)

		if form.is_valid():
			ppr = form.save(commit=False)
			ppr.requester = request.user
			ppr.save()
		
		response = {}
		return HttpResponse(simplejson.dumps(response), content_type="application/json")	
	else:
		return redirect('PubSite.views.permission_denied')

@permission_required('Philanthropy.add_hoursrecord', login_url='PubSite.views.permission_denied')
def manage_hours(request):
	"""
		Provides a view for managing hours
	"""
	
	hours_records = HoursRecord.objects.all().exclude(brother__groups__name='Alumni').order_by('-hours')
	hours_requests = HoursRequest.objects.all()
	hours_changes = HoursChangeRecord.objects.all().order_by('-dateChanged')
	add_brother_form = HoursAddBrotherForm()

	context = RequestContext(request, {
	'hours_records': hours_records,
	'hours_requests': hours_requests,
	'add_brother_form': add_brother_form,
	'hours_changes': hours_changes
	})

	return render(request, "secure/philanthropy_hours.html", context)

@permission_required('Philanthropy.add_hoursrecord', login_url='PubSite.views.permission_denied')
def add_hours(request, brother):
	"""
		View for adding hours to a given brother.
	"""
	if request.method == 'POST':
		try:
			hours = int(strip_tags(request.POST['hours']))
			changeRecord = HoursChangeRecord()
			record = HoursRecord.objects.filter(pk=brother)
			if record.exists():
				targetRecord = record[0]
				old_hours = targetRecord.hours
				targetRecord.hours = hours
				targetRecord.save()

				changeRecord.oldValue = old_hours
			else:
				user = User.objects.get(pk=brother)
				targetRecord = HoursRecord(brother=user)
				targetRecord.hours = hours
				targetRecord.save()
				changeRecord.oldValue = 0
		except:
			return redirect('PubSite.views.permission_denied')

		changeRecord.brother = targetRecord
		changeRecord.modifier = request.user
		changeRecord.dateChanged = datetime.now()
		changeRecord.newValue = targetRecord.hours
		changeRecord.save()

		response = {}
		response['id'] = targetRecord.pk
		response['name'] = targetRecord.brother.first_name + ' ' + targetRecord.brother.last_name
		response['old_hours'] = changeRecord.oldValue
		response['hours'] = targetRecord.hours
		response['date'] = dateformat.format(changeRecord.dateChanged, 'F j, Y, P')
		response['modifier'] = changeRecord.modifier.first_name + ' ' + changeRecord.modifier.last_name

		return HttpResponse(simplejson.dumps(response), content_type="application/json")
	else:
		return redirect('PubSite.views.permission_denied')

@permission_required('Philanthropy.delete_hoursrequest', login_url='PubSite.views.permission_denied')
def accept_request(request, hoursreq):
	"""
		View for accepting hours request
	"""

	if request.method == 'POST':
		hr = HoursRequest.objects.get(pk=hoursreq)
		hoursAwarded = hr.hours
		record = HoursRecord.objects.filter(pk=hr.requester)
		changeRecord = HoursChangeRecord()

		targetRecord = record[0]
		changeRecord.oldValue = targetRecord.hours
		targetRecord.hours = targetRecord.hours + hoursAwarded
		targetRecord.save()

		changeRecord.brother = targetRecord
		changeRecord.modifier = request.user
		changeRecord.dateChanged = datetime.now()
		changeRecord.newValue = targetRecord.hours
		changeRecord.save()

		hr.delete()

		response = {}
		response['id'] = targetRecord.pk
		response['name'] = targetRecord.brother.first_name + ' ' + targetRecord.brother.last_name
		response['old_hours'] = changeRecord.oldValue
		response['hours'] = targetRecord.hours
		response['date'] = dateformat.format(changeRecord.dateChanged, 'F j, Y, P')
		response['modifier'] = changeRecord.modifier.first_name + ' ' + changeRecord.modifier.last_name

		return HttpResponse(simplejson.dumps(response), content_type="application/json")
	else:
		return redirect('PubSite.views.permission_denied')

@permission_required('Philanthropy.delete_hoursrequest', login_url='PubSite.views.permission_denied')
def delete_request(request, hoursreq):
	"""
		View for denying hours request
	"""

	if request.method == 'POST':
		request = HoursRequest.objects.get(pk=hoursreq)
		request.delete()

	response = {}
	return HttpResponse(simplejson.dumps(response), content_type="application/json")

@permission_required('Philanthropy.delete_hoursrequest', login_url='PubSite.views.permission_denied')
def reset_hours(request):
	"""
		View for resetting all hours
	"""
	if request.method == 'POST':
		records = HoursRecord.objects.all().delete()

	response = {}
	return HttpResponse(simplejson.dumps(response), content_type="application/json")
