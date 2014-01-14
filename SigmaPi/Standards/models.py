from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.forms import ModelChoiceField
from datetime import datetime

class CustomModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.first_name + " " + obj.last_name

class Bone(models.Model):
	"""
		Model for a single bone that is given to a User
	"""
	bonee = models.ForeignKey(User, related_name="bonee")
	boner = models.ForeignKey(User, related_name="boner")
	reason = models.TextField()
	dateReceived = models.DateField()
	expirationDate = models.DateField()

	def __unicode__(self):
		return self.reason

	class Meta:
		verbose_name = "Bone"
		verbose_name_plural = "Bones"

class BoneChangeRecord(models.Model):
	"""
		Model for a bone change history record
	"""
	bone = models.ForeignKey(Bone)
	modifier = models.ForeignKey(User)
	dateChangeMade = models.DateTimeField()
	previousReason = models.TextField()
	newReason = models.TextField()
	previousExpirationDate = models.DateField()
	newExpirationDate = models.DateField()

	def __unicode__(self):
		return self.bone

	class Meta:
		verbose_name = "Bone Change Record"
		verbose_name_plural = "Bone Change Records"


class Probation(models.Model):
	"""
		Model for a probation punishment that a user will receive.
	"""
	recipient = models.ForeignKey(User, related_name="recipient")
	giver = models.ForeignKey(User, related_name='giver')
	dateReceived = models.DateField()
	expirationDate = models.DateField()

	def __unicode__(self):
		return self.recipient

	class Meta:
		verbose_name = "Probation"
		verbose_name_plural = "Probations"

class PiPointsRecord(models.Model):
	"""
		Model for a pipoint record for a user
	"""
	brother = models.OneToOneField(User, primary_key=True)
	points = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return self.user

	class Meta:
		verbose_name = "Pi Points Record"
		verbose_name_plural = "Pi Points Records"

class PiPointsChangeRecord(models.Model):
	"""
		Model for a PiPoint change history record
	"""
	brother = models.ForeignKey(User, related_name="brother")
	modifier = models.ForeignKey(User, related_name="modifier")
	dateChanged = models.DateTimeField()
	oldValue = models.PositiveIntegerField(default=0)
	newValue = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return self.dateChanged

	class Meta:
		verbose_name = "Pi Points Change Record"
		verbose_name_plural = "Pi Points Change Records"

class PiPointsRequest(models.Model):
	"""
		Model for a request for pi points
	"""
	requester = models.ForeignKey(User)
	reason = models.TextField()
	witness = models.CharField(max_length=100, default="None")
	
	def __unicode__(self):
		return self.requester

	class Meta:
		verbose_name = "Pi Points Request"
		verbose_name_plural = "Pi Points Request"

class PiPointsRequestForm(ModelForm):
	"""
		Form for requesting pipoints
	"""

	reason = forms.CharField(widget=forms.Textarea)
	witness = forms.CharField(max_length=100, required=False)

	class Meta:
		model = PiPointsRequest
		exclude = ['requester']

class BoneGivingForm(ModelForm):
	"""
		Form for giving Bones
	"""
	bonee = CustomModelChoiceField(queryset=User.objects.all().order_by('last_name').exclude(groups__name='Alumni'))
	reason = forms.CharField(widget=forms.Textarea)
	expirationDate = models.DateField()

	class Meta:
		model = Bone
		exclude = ['boner', 'dateReceived']

class ProbationGivingForm(ModelForm):
	"""
		Form for giving probation
	"""
	recipient = CustomModelChoiceField(queryset=User.objects.all().order_by('last_name').exclude(groups__name='Alumni'))
	expirationDate = models.DateField()

	class Meta:
		model = Probation
		exclude = ['giver', 'dateReceived']

