from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm, ValidationError

import datetime
import re


def validate_date(date):
	if date > datetime.date.today():
		raise ValidationError("The date given cannot be in the future.")


def validate_number(number):
	if number < 0:
		raise ValidationError("The number given cannot be negative.")


def occurred_this_week(date):
	one_week_delta = datetime.timedelta(days=7)
	today_date = datetime.date.today()
	today_date_weekday_number = today_date.weekday()
	beginning_of_week_monday = today_date - datetime.timedelta(days=today_date_weekday_number)
	next_monday = beginning_of_week_monday + one_week_delta

	return beginning_of_week_monday <= date < next_monday

class TrackedUser(models.Model):
	"""
		Model for a user who currently has their study hours tracked.
	"""

	def __unicode__(self):
		return self.user.__str__()

	def __str__(self):
		return self.user.__str__()

	def hours_this_week(self):
		this_users_records = StudyHoursRecord.objects.filter(user=self.user)
		return sum([record.number_of_hours for record in this_users_records if occurred_this_week(record.date)])

	def save(self, *args, **kwargs):
		existing_entry = TrackedUser.objects.filter(user=self.user)

		if existing_entry.count() != 0:
			existing_entry.update(number_of_hours=self.number_of_hours)
			return

		else:
			# Call the "real" save() method.
			super(TrackedUser, self).save(*args, **kwargs)


	# Fields for this model.
	user = models.ForeignKey(User)
	number_of_hours = models.IntegerField(validators=[validate_number])

	# Meta information about this model.
	class Meta:

		# New permission definitions
		permissions = (
			("scholarship_head", "Can add/modify which users have their study hours tracked."),
		)


class TrackedUserForm(ModelForm):
	class Meta:
		model = TrackedUser
		fields = ['user', 'number_of_hours']


class StudyHoursRecord(models.Model):
	"""
		Model for a record of study hours made by one tracked user for one day.
	"""

	def __unicode__(self):
		return "Study hours by " + self.tracked_user.__str__() + " on " + self.date.__str__()

	def __str__(self):
		return "Study hours by " + self.tracked_user.__str__() + " on " + self.date.__str__()

	def happened_this_week(self):
		return occurred_this_week(self.date)

	# Fields for this model.
	user = models.ForeignKey(User)
	number_of_hours = models.IntegerField(validators=[validate_number])
	date = models.DateField(validators=[validate_date])
	time_stamp = models.DateTimeField(auto_now_add=True, editable=False)


class StudyHoursRecordForm(ModelForm):
	class Meta:
		model = StudyHoursRecord
		fields = ['number_of_hours', 'date']


class TestScan(models.Model):
	"""
		Model for a test scan.
	"""

	def __unicode__(self):
		return str(self.course_number) + ": " + str(self.name)

	def __str__(self):
		return str(self.course_number) + ": " + str(self.name)

	def clean(self):
		# Strip all non alpha-numeric characters from the class name
		if self.course_number:
			self.course_number = self.course_number.strip()
			self.course_number = re.sub(r'\W+', '', self.course_number)

	test_name = models.CharField(max_length=100)
	course_number = models.CharField(max_length=100)
	professor_name = models.CharField(max_length=100)
	test_pdf = models.FileField(upload_to='protected/library/tests' + str(course_number) + "_" + re.sub(r'\W+', '_', str(test_name)))

	year = models.IntegerField(blank=True)
	term = models.CharField(blank=True, max_length=1,   \
	                        choices = (('A','A Term'),  \
										('B','B Term'), \
										('C','C Term'), \
										('D','D Term'), \
										('E','E Term')))


class TestScanForm(ModelForm):
	class Meta:
		model = TestScan
		fields = ['test_name', 'course_number', 'professor_name', 'test_pdf', 'year', 'term']
