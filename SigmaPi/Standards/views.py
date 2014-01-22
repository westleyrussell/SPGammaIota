from django.template import RequestContext
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.utils.html import strip_tags
from django.utils import simplejson, dateformat

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User

from datetime import datetime

from Standards.models import JobRequest, JobRequestForm, Bone, PiPointsRecord, PiPointsRequest, PiPointsChangeRecord, PiPointsRequestForm, PiPointsAddBrotherForm, Probation, BoneChangeRecord, ProbationGivingForm, BoneGivingForm, BoneEditingForm

@login_required
def index(request, error=None):
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
	job_givers = JobRequest.objects.filter(takingJob=False).exclude(requester=request.user)
	job_doers = JobRequest.objects.filter(takingJob=True).exclude(requester=request.user)
	own_givers = JobRequest.objects.filter(takingJob=False, requester=request.user)
	own_doers = JobRequest.objects.filter(takingJob=True, requester=request.user)
	jobs_form = JobRequestForm()

	requests_count = JobRequest.objects.all().count()
	pprCount = PiPointsRequest.objects.all().count()
	positive_points = own_points.points > 0

	context = RequestContext(request, {
	'current_bone_count': current_bone_count,
	'current_bones': current_bones,
	'expired_bones': expired_bones,
	'own_points': own_points,
	'point_records': point_records,
	'probation': probation,
	'points_form': points_form,
	'job_givers':job_givers,
	'job_doers':job_doers,
	'own_doers': own_doers,
	'own_givers': own_givers,
	'jobs_form': jobs_form,
	'positive_points': positive_points,
	'error': error,
	'requests_count': requests_count,
	'pprCount': pprCount
	})

	return render(request, "secure/standards_index.html", context)

@permission_required('Standards.add_pipointsrequest', login_url='PubSite.views.permission_denied')
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
	pprCount = PiPointsRequest.objects.all().count()
	
	context = RequestContext(request, {
	'active_bones': all_bones,
	'expired_bones': expired_bones,
	'all_probations': all_probations,
	'probation_form': probation_form,
	'bone_form': bone_form,
	'bone_edit_history': bone_edit_history,
	'pprCount': pprCount
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
		form = BoneEditingForm(request.POST, instance=targetBone)

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
			bone_form = BoneEditingForm(instance=targetBone)
		else:
			bone_form = None
		pprCount = PiPointsRequest.objects.all().count()
		context = RequestContext(request, {
			'bone': targetBone,
			'expired': expired,
			'bone_form': bone_form,
			'bone_history': bone_history,
			'pprCount': pprCount
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

@login_required
def reduce_bone(request, bone):
	"""
		View for reducing a bone.
	"""
	if request.method == 'POST':
		targetBone = Bone.objects.get(pk=bone)

		if not targetBone.bonee == request.user:
			return redirect('PubSite.views.permission_denied')
		else:
			pointsRecord = PiPointsRecord.objects.get(brother=request.user)

			if pointsRecord.points <= 0:
				return redirect('Standards.views.index')
			elif pointsRecord.points < targetBone.value:
				targetBone.value = targetBone.value - pointsRecord.points
				targetBone.save()
				pointsRecord.points = 0
				pointsRecord.save()
			else:
				pointsRecord.points = pointsRecord.points - targetBone.value
				pointsRecord.save()
				targetBone.expirationDate = datetime.now()
				targetBone.save()

			return redirect('Standards.views.index')
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

		response = {}
		return HttpResponse(simplejson.dumps(response), content_type="application/json")
	else:
		return redirect('PubSite.views.permission_denied')


@permission_required('Standards.add_pipointsrecord', login_url='PubSite.views.permission_denied')
def manage_points(request):
	"""
		Provides a view for managing pi points
	"""
	
	point_records = PiPointsRecord.objects.all().exclude(brother__groups__name='Alumni').order_by('-points')
	point_requests = PiPointsRequest.objects.all()
	point_changes = PiPointsChangeRecord.objects.all().order_by('-dateChanged')
	add_brother_form = PiPointsAddBrotherForm()
	pprCount = PiPointsRequest.objects.all().count()
	
	context = RequestContext(request, {
	'point_records': point_records,
	'point_requests': point_requests,
	'add_brother_form': add_brother_form,
	'point_changes': point_changes,
	'pprCount': pprCount,
	})

	return render(request, "secure/standards_points.html", context)

@permission_required('Standards.add_pipointsrecord', login_url='PubSite.views.permission_denied')
def add_points(request, brother):
	"""
		View for adding points to a given brother.
	"""
	if request.method == 'POST':
		try:
			points = int(strip_tags(request.POST['piPoints']))
			changeRecord = PiPointsChangeRecord()
			record = PiPointsRecord.objects.filter(pk=brother)
			if record.exists():
				targetRecord = record[0]
				old_points = targetRecord.points
				targetRecord.points = points
				targetRecord.save()

				changeRecord.oldValue = old_points
			else:
				user = User.objects.get(pk=brother)
				targetRecord = PiPointsRecord(brother=user)
				targetRecord.points = points
				targetRecord.save()
				changeRecord.oldValue = 0
		except:
			return redirect('PubSite.views.permission_denied')

		changeRecord.brother = targetRecord
		changeRecord.modifier = request.user
		changeRecord.dateChanged = datetime.now()
		changeRecord.newValue = targetRecord.points
		changeRecord.save()

		response = {}
		response['id'] = targetRecord.pk
		response['name'] = targetRecord.brother.first_name + ' ' + targetRecord.brother.last_name
		response['old_points'] = changeRecord.oldValue
		response['points'] = targetRecord.points
		response['date'] = dateformat.format(changeRecord.dateChanged, 'F j, Y, P')
		response['modifier'] = changeRecord.modifier.first_name + ' ' + changeRecord.modifier.last_name

		return HttpResponse(simplejson.dumps(response), content_type="application/json")
	else:
		return redirect('PubSite.views.permission_denied')

@permission_required('Standards.delete_pipointsrequest', login_url='PubSite.views.permission_denied')
def accept_request(request, pointreq):
	"""
		View for accepting points request
	"""

	if request.method == 'POST':
		ppr = PiPointsRequest.objects.get(pk=pointreq)
		pointsAwarded = ppr.pointsForReason(ppr.reason)
		record = PiPointsRecord.objects.filter(pk=ppr.requester)
		changeRecord = PiPointsChangeRecord()

		targetRecord = record[0]
		changeRecord.oldValue = targetRecord.points
		targetRecord.points = targetRecord.points + pointsAwarded
		targetRecord.save()

		changeRecord.brother = targetRecord
		changeRecord.modifier = request.user
		changeRecord.dateChanged = datetime.now()
		changeRecord.newValue = targetRecord.points
		changeRecord.save()

		ppr.delete()

		response = {}
		response['id'] = targetRecord.pk
		response['name'] = targetRecord.brother.first_name + ' ' + targetRecord.brother.last_name
		response['old_points'] = changeRecord.oldValue
		response['points'] = targetRecord.points
		response['date'] = dateformat.format(changeRecord.dateChanged, 'F j, Y, P')
		response['modifier'] = changeRecord.modifier.first_name + ' ' + changeRecord.modifier.last_name
		response['pprCount'] = PiPointsRequest.objects.all().count()
		return HttpResponse(simplejson.dumps(response), content_type="application/json")
	else:
		return redirect('PubSite.views.permission_denied')

@permission_required('Standards.delete_pipointsrequest', login_url='PubSite.views.permission_denied')
def delete_request(request, pointreq):
	"""
		View for denying points request
	"""

	if request.method == 'POST':
		request = PiPointsRequest.objects.get(pk=pointreq)
		request.delete()

	response = {}
	response['pprCount'] = PiPointsRequest.objects.all().count()
	return HttpResponse(simplejson.dumps(response), content_type="application/json")

@login_required
def add_job_request(request, jobtype):

	if request.method == 'POST':
		form = JobRequestForm(request.POST)
		takingJob = jobtype == '2'

		pipoints = PiPointsRecord.objects.get(brother=request.user)
		response = {}

		if form.is_valid():
			jobreq = form.save(commit=False)

			# If looking for cover, make sure we have enough pi points
			if not takingJob:
				cost = jobreq.REASON_POINTS[jobreq.job]
				if cost > pipoints.points:
					response['error'] = 'Could not submit job request, you do not have enough Pi Points!'
					return HttpResponse(simplejson.dumps(response), content_type="application/json") 
				else:
					# Check all outstanding requests
					all_req = JobRequest.objects.filter(requester=request.user, takingJob=False)
					runningTally = cost
					for req in all_req:
						runningTally = runningTally + req.REASON_POINTS[req.job]
						if runningTally > pipoints.points:
							response['error'] = 'Could not submit job request.  You do not have enough Pi Points to satisfy all your outstanding requests.'
							return HttpResponse(simplejson.dumps(response), content_type="application/json") 

			jobreq.requester = request.user
			jobreq.takingJob = takingJob
			jobreq.save()

			response['requestCount'] = JobRequest.objects.all().count()
			response['takingJob'] = jobreq.takingJob
			response['requester'] = jobreq.requester.first_name + " " + jobreq.requester.last_name
			response['job'] = jobreq.get_job_display()
			response['details'] = jobreq.details
			response['id'] = jobreq.pk
		else:
			response['error'] = form.errors

		return HttpResponse(simplejson.dumps(response), content_type="application/json") 
	else:
		return redirect('PubSite.views.permission_denied')

@login_required
def delete_job_request(request, jobrequest):
	if request.method == 'POST':
		try:
			jobreq = JobRequest.objects.get(pk=jobrequest)
		except:
			response = {}
			ppr = PiPointsRecord.objects.get(brother=request.user)
			response['error'] = "Sorry, that request cannot be deleted.  Somebody has already accepted the request."
			response['points'] = ppr.points
			response['requestCount'] = JobRequest.objects.all().count()
			return HttpResponse(simplejson.dumps(response), content_type="application/json") 

		if jobreq.requester == request.user:
			jobreq.delete()

			ppr = PiPointsRecord.objects.get(brother=request.user)
			response = {}
			response['points'] = ppr.points
			response['requestCount'] = JobRequest.objects.all().count()
			return HttpResponse(simplejson.dumps(response), content_type="application/json") 
		else:
			return redirect('PubSite.views.permission_denied')
	else:
		return redirect('PubSite.views.permission_denied')

@login_required
def accept_job_request(request, jobrequest):
	"""
		When a job request is accepted:
			A Pi Point request is sent for the user who is covering the job.
			The user whose job is being covered is docked pi points
			the request is deleted
	"""

	if request.method == 'POST':
		try:
			jobreq = JobRequest.objects.get(pk=jobrequest)
		except:
			response = {}
			response['error'] = "Sorry, that request no longer exists.  Either the person who put it up deleted it or somebody else already accepted it."
			response['delete'] = True
			response['requestCount'] = JobRequest.objects.all().count()
			return HttpResponse(simplejson.dumps(response), content_type="application/json") 

		# If its a job request where the requester is taking the job, they'll get the pi points
		if jobreq.takingJob:

			# Check that the giver has enough points
			takingBrother = jobreq.requester
			giverRecord = PiPointsRecord.objects.get(brother=request.user)
			currentRecord = giverRecord
			if giverRecord.points < jobreq.REASON_POINTS[jobreq.job]:
				response = {}
				response['error'] = "You do not have enough Pi Points to have someone cover this job."
				return HttpResponse(simplejson.dumps(response), content_type="application/json") 

		else:
			takingBrother = request.user
			giverRecord = PiPointsRecord.objects.get(brother=jobreq.requester)
			currentRecord = PiPointsRecord.objects.get(brother=request.user)

		# Send a request for the taker
		ppr = PiPointsRequest()
		ppr.requester = takingBrother
		ppr.reason = jobreq.job
		ppr.witness = "Took a job through Pi Point Web System."
		ppr.save()

		# Subtract pi points from giver
		giverRecord.points = giverRecord.points - jobreq.REASON_POINTS[jobreq.job]
		giverRecord.save()

		alertAboutJob(giverRecord, takingBrother, jobreq.get_job_display(), jobreq.details)

		jobreq.delete()
		response = {}
		response['points'] = currentRecord.points
		response['requestCount'] = JobRequest.objects.all().count()
		return HttpResponse(simplejson.dumps(response), content_type="application/json") 
	else:
		return redirect('PubSite.views.permission_denied')

def alertAboutJob(giverRecord, takerUser, jobTitle, jobDetails):
	takerName = takerUser.first_name + " " + takerUser.last_name
	giverName = giverRecord.brother.first_name + " " + giverRecord.brother.last_name
	subject_to_giver = takerName + " has taken your job: " + jobTitle + "!"
	message_to_giver = takerName + " has volunteered to perform your job: " + jobTitle + "."
	message_to_giver = message_to_giver + " Please coordinate with him so that you may ensure the job is"
	message_to_giver = message_to_giver + " completed correctly and on time.  Thank you from the Standards Board."

	subject_to_taker = "You have been assigned to take " + giverName +"'s job: " jobTitle + "!"
	message_to_taker = "Please ensure that you complete the job correctly and on time.  Failure to do so"
	message_to_taker = message_to_taker + " may result in a loss of Pi Points and/or a summons.  Please "
	message_to_taker = message_to_taker + "coordinate with " + giverName + " concerning the details of the job."
	message_to_taker = message_to_taker + " Thank you from the Standards Board."

	send_mail(subject_to_giver, message_to_giver, settings.DEFAULT_FROM_EMAIL, [giverRecord.brother.email])
	send_mail(subject_to_taker, message_to_taker, settings.DEFAULT_FROM_EMAIL, [takerUser.email])



