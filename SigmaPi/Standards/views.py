from django.template import RequestContext
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.utils import simplejson

from django.contrib.auth.decorators import permission_required, login_required

from datetime import datetime


from Standards.models import Bone, PiPointsRecord, PiPointsRequestForm, Probation, BoneChangeRecord, ProbationGivingForm, BoneGivingForm

@login_required
def index(request):
	"""
		Displays the homepage of the standards module.
	"""

	bones = Bone.objects.filter(bonee=request.user)
	current_bone_count = Bone.objects.filter(bonee=request.user, expirationDate__gt=datetime.now()).count()
	
	point_records = PiPointsRecord.objects.all().exclude(brother__groups__name='Alumni').order_by('points')
	
	own_points = PiPointsRecord.objects.filter(brother=request.user)

	if own_points.count() == 0:
		# If we don't have a record, create one.
		record = PiPointsRecord()
		record.points = 0
		record.brother = request.user
		record.save()
		own_points = record
	else:
		own_points = own_points[0]

	probation = Probation.objects.filter(recipient=request.user, expirationDate__gt=datetime.now())
	probation = probation.count() > 0

	points_form = PiPointsRequestForm()

	context = RequestContext(request, {
	'current_bone_count': current_bone_count,
	'bones': bones,
	'own_points': own_points,
	'point_records': point_records,
	'probation': probation,
	'points_form': points_form,
	})

	return render(request, "secure/standards_index.html", context)

@login_required
def request_points(request):
	"""
		Registers a pi point request to be reviewed by the friendly neighborhood parliamentarian
	"""
	if request.method == 'POST':
		form = PiPointsRequestForm(request.POST)

		if form.is_valid():
			ppr = form.save(commit=False)
			ppr.requester = request.user
			ppr.save()
		
		response = {}
		return HttpResponse(simplejson.dumps(response), content_type="application/json")	
	else:
		return redirect('PubSite.views.permission_denied')

@permission_required('Standards.add_bone', login_url='PubSite.views.permission_denied')
def edit_bones(request):
	"""
		View for editing/managing all bones and punishments
	"""

	all_bones = Bone.objects.all().order_by('dateReceived')
	all_probations = Probation.objects.all().order_by('dateReceived')
	bone_edit_history = BoneChangeRecord.objects.all().order_by('dateChangeMade')
	probation_form = ProbationGivingForm()
	bone_form = BoneGivingForm()

	context = RequestContext(request, {
	'all_bones': all_bones,
	'all_probations': all_probations,
	'probation_form': probation_form,
	'bone_form': bone_form,
	'bone_edit_history': bone_edit_history
	})

	return render(request, "secure/standards_bones.html", context)

@permission_required('Standards.add_bone', login_url='PubSite.views.permission_denied')
def edit_bone(request, bone):
	pass

@permission_required('Standards.add_bone', login_url='PubSite.views.permission_denied')
def add_bone(request):
	"""
		View for adding a new bone.
	"""
	if request.method == 'POST':
		form = BoneGivingForm(request.POST)

		if form.is_valid():
			bone = form.save(commit=False)
			bone.boner = request.user
			bone.dateReceived = datetime.now()
			bone.save()

		return redirect('Standards.views.edit_bones')
	else:
		return redirect('PubSite.views.permission_denied')

@permission_required('Standards.add_probation', login_url='PubSite.views.permission_denied')
def add_probation(request):
	"""
		View for adding a new probation.
	"""
	if request.method == 'POST':
		form = ProbationGivingForm(request.POST)

		if form.is_valid():
			probation = form.save(commit=False)
			probation.giver = request.user
			probation.dateReceived = datetime.now()
			probation.save()

		return redirect('Standards.views.edit_bones')
	else:
		return redirect('PubSite.views.permission_denied')

@permission_required('Standards.add_pipointsrecord', login_url='PubSite.views.permission_denied')
def edit_points(request):
	pass

@permission_required('Standards.add_pipointsrecord', login_url='PubSite.views.permission_denied')
def add_points(request, brother):
	pass



