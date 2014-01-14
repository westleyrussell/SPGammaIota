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

	current_bones = Bone.objects.filter(bonee=request.user, expirationDate__gt=datetime.now()).order_by('-expirationDate')
	expired_bones = Bone.objects.filter(bonee=request.user, expirationDate__lte=datetime.now()).order_by('-expirationDate')
	current_bone_count = current_bones.count()
	
	point_records = PiPointsRecord.objects.all().exclude(brother__groups__name='Alumni').order_by('-points')
	
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

	probation = Probation.objects.filter(recipient=request.user, expirationDate__gt=datetime.now()).exists()
	points_form = PiPointsRequestForm()

	context = RequestContext(request, {
	'current_bone_count': current_bone_count,
	'current_bones': current_bones,
	'expired_bones': expired_bones,
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

	all_bones = Bone.objects.filter(expirationDate__gt=datetime.now()).order_by('-dateReceived')
	expired_bones = Bone.objects.filter(expirationDate__lte=datetime.now())
	all_probations = Probation.objects.filter(expirationDate__gt=datetime.now()).order_by('-dateReceived')

	bone_edit_history = BoneChangeRecord.objects.all().order_by('-dateChangeMade')
	probation_form = ProbationGivingForm()
	bone_form = BoneGivingForm()

	context = RequestContext(request, {
	'active_bones': all_bones,
	'expired_bones': expired_bones,
	'all_probations': all_probations,
	'probation_form': probation_form,
	'bone_form': bone_form,
	'bone_edit_history': bone_edit_history
	})

	return render(request, "secure/standards_bones.html", context)

@permission_required('Standards.change_bone', login_url='PubSite.views.permission_denied')
def edit_bone(request, bone):
	"""
		View for editing a single bone.
	"""

	try:
		targetBone = Bone.objects.get(pk=bone)
		expired = targetBone.expirationDate <= datetime.now().date()
	except:
		return redirect('PubSite.views.permission_denied')

	if request.method == 'POST':
		if expired:
			return redirect('PubSite.views.permission_denied')

		oldReason = targetBone.reason
		oldPerson = targetBone.bonee
		oldExpiration = targetBone.expirationDate
		form = BoneGivingForm(request.POST, instance=targetBone)

		if form.is_valid():
			bone = form.save()
			if not bone.bonee == oldPerson:
				bone.bonee = oldPerson
				bone.save()
			record = BoneChangeRecord()
			record.bone = targetBone
			record.modifier = request.user
			record.dateChangeMade = datetime.now()
			record.previousReason = oldReason
			record.newReason = targetBone.reason
			record.previousExpirationDate = oldExpiration
			record.newExpirationDate = targetBone.expirationDate
			record.save()

		return redirect('Standards.views.edit_bones')
	else:
		bone_history = BoneChangeRecord.objects.filter(bone=targetBone).order_by('-dateChangeMade')

		if not expired:
			bone_form = BoneGivingForm(instance=targetBone)
		else:
			bone_form = None

		context = RequestContext(request, {
			'bone': targetBone,
			'expired': expired,
			'bone_form': bone_form,
			'bone_history': bone_history
			})

		return render(request, "secure/standards_edit_bone.html", context)

@permission_required('Standards.delete_bone', login_url='PubSite.views.permission_denied')
def expire_bone(request, bone):
	"""
		View for expiring a single bone.
	"""

	try:
		targetBone = Bone.objects.get(pk=bone)
		expired = targetBone.expirationDate <= datetime.now().date()
	except:
		return redirect('PubSite.views.permission_denied')

	if request.method == 'POST':
		if expired:
			return redirect('PubSite.views.permission_denied')

		oldExpirationDate = targetBone.expirationDate
		targetBone.expirationDate = datetime.now()
		targetBone.save()

		record = BoneChangeRecord()
		record.bone = targetBone
		record.modifier = request.user
		record.dateChangeMade = datetime.now()
		record.previousReason = targetBone.reason
		record.newReason = targetBone.reason
		record.previousExpirationDate = oldExpirationDate
		record.newExpirationDate = targetBone.expirationDate
		record.save()

		return redirect('Standards.views.edit_bones')
	else:
		return redirect('Standards.views.edit_bones')

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

			record = BoneChangeRecord()
			record.bone = bone
			record.modifier = request.user
			record.dateChangeMade = datetime.now()
			record.previousReason = "CREATED"
			record.newReason = bone.reason
			record.previousExpirationDate = bone.expirationDate
			record.newExpirationDate = bone.expirationDate
			record.save()

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

@permission_required('Standards.delete_probation', login_url='PubSite.views.permission_denied')
def end_probation(request, probation):
	"""
		View for ending a social probation.
	"""
	if request.method == 'POST':
		probation = Probation.objects.get(pk=probation)
		probation.expirationDate = datetime.now()
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



