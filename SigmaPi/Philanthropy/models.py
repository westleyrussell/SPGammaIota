from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, Form
from django.forms import ModelChoiceField
from datetime import datetime

class CustomModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.first_name + " " + obj.last_name

class HoursRecord(models.Model):
	"""
		Model for a pipoint record for a user
	"""
	brother = models.OneToOneField(User, primary_key=True)
	hours = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return self.user

	class Meta:
		verbose_name = "Hours Record"
		verbose_name_plural = "Hours Records"

class HoursChangeRecord(models.Model):
	"""
		Model for a hours change history record
	"""
	brother = models.ForeignKey(HoursRecord)
	modifier = models.ForeignKey(User)
	dateChanged = models.DateTimeField()
	oldValue = models.PositiveIntegerField(default=0)
	newValue = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return self.dateChanged

	class Meta:
		verbose_name = "Pi Points Change Record"
		verbose_name_plural = "Pi Points Change Records"

class HoursRequest(models.Model):
	"""
		Model for a request for hours
	"""
	requester = models.ForeignKey(User)
	hours = models.PositiveIntegerField(default=0)
	activity = models.CharField(max_length=100, default="None")
	description = models.CharField(max_length=10000, default="None")

	def __unicode__(self):
		return self.requester

	class Meta:
		verbose_name = "Hours Request"
		verbose_name_plural = "Hours Request"

class HoursRequestForm(ModelForm):
	"""
		Form for requesting hours
	"""
	hours = forms.CharField()
	activity = forms.CharField(max_length=100)
	description = forms.CharField(widget=forms.Textarea, required=False)

	class Meta:
		model = HoursRequest
		exclude = ['requester']

class HoursAddBrotherForm(Form):
	"""
		Form for adding a brother to the hours system
	"""
	brother = CustomModelChoiceField(queryset=User.objects.all().order_by('last_name').exclude(groups__name='Alumni').exclude(pipointsrecord__isnull=False))
	hours = forms.IntegerField(min_value=0)
