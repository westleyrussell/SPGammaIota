from django.template import RequestContext
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import permission_required, login_required

from datetime import datetime

@login_required
def index(request):
	"""
		Displays the homepage of the standards module.
	"""
	bones = Bone.objects.filter(bonee=request.User)
	point_records = PiPointsRecord.objects.all().exclude(brother__groups__name='Alumni').order_by('points')
	
	own_points = PiPointsRecord.objects.filter(brother=request.User)
	probation = Probation.objects.filter(recipient=request.User)

	context = RequestContext(request, {
	'bones': bones,
	'own_points': own_points
	'point_records': point_records,
	'probation': probation
	})

	return render(request, "secure/standards_index.html", context)

@login_required
def request_points(request):
	pass

@permission_required('Standards.add_bone', login_url='PubSite.views.permission_denied')
def edit_bones(request):
	pass

@permission_required('Standards.add_pipointsrecord', login_url='PubSite.views.permission_denied')
def edit_points(request):
	pass



