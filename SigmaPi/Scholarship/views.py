from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_GET, require_POST

from Scholarship.models import TrackedUser, TrackedUserForm, StudyHoursRecord, StudyHoursRecordForm, TestScan, TestScanForm


def request_is_from_tracked_user(request):
	"""
		Returns true if the request is from a user who is required to log more
		than 0 study hours per week.
	"""
	return TrackedUser.objects.filter(number_of_hours__gt=0, user=request.user).count() == 1


def request_is_from_scholarship_head(request):
	"""
		Returns true if the request from the scholarship head user.
	"""
	return request.user.has_perm('Scholarship.scholarship_head')


def get_currently_tracked_users():
	"""
		Returns a queryset of TrackedUser's who are required to record more than
		0 study hours per week.
	"""
	return TrackedUser.objects.filter(number_of_hours__gt=0)


@login_required
@require_GET
def index(request):
	"""
		Navigation to the index with redirect to:

		- The Study Hours page if the request if from the scholarship head or
		  from a user who currently has their study hours tracked.
		- The Test Scans page otherwise.
	"""

	if request_is_from_scholarship_head(request) or request_is_from_tracked_user(request):
		return redirect('Scholarship.views.study_hours')

	return redirect('Scholarship.views.tests')


@login_required
@require_GET
def study_hours(request):

	# Figure out if this request is from the scholarship head
	is_scholarship_head = request_is_from_scholarship_head(request)

	# Figure out if this request is from a user who currently has their
	# study hours tracked
	is_tracked_user = request_is_from_tracked_user(request)

	# Initialize objects if necessary for the scholarship head
	currently_tracked_users = None
	update_requirements_form = None
	if is_scholarship_head:
		currently_tracked_users = get_currently_tracked_users()
		update_requirements_form = TrackedUserForm()

	# Initialize objects if necessary for a tracked user
	record_hours_form = None
	tracked_user_object = None
	tracked_user_records_this_week = None
	if is_tracked_user:
		record_hours_form = StudyHoursRecordForm()
		tracked_user_object = TrackedUser.objects.get(user=request.user)
		tracked_user_records = StudyHoursRecord.objects.filter(user=request.user).order_by('-date')
		tracked_user_records_this_week = [record for record in tracked_user_records if record.happened_this_week()]

	context = RequestContext(request, {
		'is_scholarship_head': is_scholarship_head,
		'is_tracked_user': is_tracked_user,
		'currently_tracked_users': currently_tracked_users,
		'update_requirements_form': update_requirements_form,
		'record_hours_form': record_hours_form,
		'tracked_user_object': tracked_user_object,
		'tracked_user_records_this_week': tracked_user_records_this_week
	})

	return render(request, "scholarship_study_hours.html", context)

@permission_required('Scholarship.scholarship_head', login_url='PubSite.views.permission_denied')
@require_POST
def update_requirements(request):

	update_requirements_form = TrackedUserForm(request.POST)

	if update_requirements_form.is_valid():
		update_requirements_form.save()

	return redirect("Scholarship.views.study_hours")


@login_required
@require_POST
def record_hours(request):
	record_hours_form = StudyHoursRecordForm(request.POST)

	if record_hours_form.is_valid():
		study_hours_record = record_hours_form.save(commit=False)
		study_hours_record.user = request.user
		study_hours_record.save()

	return redirect("Scholarship.views.study_hours")


@login_required
@require_GET
def tests(request):

	is_scholarship_head = request_is_from_scholarship_head(request)

	upload_test_form = None
	if is_scholarship_head:
		upload_test_form = TestScanForm()

	test_scans = TestScan.objects.all()

	context = RequestContext(request, {
		'is_scholarship_head': is_scholarship_head,
		'upload_test_form': upload_test_form,
		'test_scans': test_scans
	})

	return render(request, "scholarship_tests.html", context)

@permission_required('Scholarship.scholarship_head', login_url='PubSite.views.permission_denied')
@require_POST
def upload_test(request):

	upload_test_form = TestScanForm(request.POST)

	if upload_test_form.is_valid():
		upload_test_form.save()

	return redirect("Scholarship.views.tests")

@login_required
@require_GET
def textbooks(request):
	return render(request, "scholarship_textbooks.html")

