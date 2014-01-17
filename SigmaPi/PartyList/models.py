from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import datetime

import json

def timeStamped(fname, fmt='%Y-%m-%d_{fname}'):
	"""
		Utility function to add a timestamp to uploaded files.
	"""
	return datetime.now().strftime(fmt).format(fname=fname)

class Party(models.Model):
	"""
		Model to represent a party.
	"""

	def partyjobspath(self, filename):
		"""
			Defines where bylaws should be stored
		"""
		return "protected/partyjobs/" + timeStamped(filename)

	name = models.CharField(max_length=100)
	date = models.DateField()
	guycount = models.IntegerField(default=0)
	girlcount = models.IntegerField(default=0)

	jobs = models.FileField(upload_to=partyjobspath)

	def __unicode__(self):
		return self.name

	def save(self):
		self.name = self.name.replace(" ","_")
		super(Party,self).save()

	def displayname(self):
		return self.name.replace("_"," ")

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "Parties"
		verbose_name = "Party"
		permissions = (
            ("manage_parties", "Can manage parties."),
        )

class Guest(models.Model):
	"""
		Model to represent a party guest
	"""
	name = models.CharField(max_length=100)
	birthDate = models.DateField(blank=True,auto_now=True)
	gender = models.CharField(max_length=100)
	cardID = models.CharField(max_length=100, blank=True)
	createdAt = models.DateTimeField(auto_now_add=True)
	updatedAt = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name

	def __iter__(self):
		"""return a ** iterator of field,value"""
		for i in self._meta.get_all_field_names():
			yield (i, getattr(self,i))

	def __cmp__(self,other):
		pass
		#apparently django does not use this during the order_by query

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "Guests"
		verbose_name = "Guest"

	def toJSON(self):
		"""return a json object of the guest"""
		data = {}
		for field,val in self:
			try:
				data[field] = json.dumps(val)
			except:
				pass

		return json.dumps(data)


class PartyGuest(models.Model):
	"""
		Model to represent a guest for a specific party.
	"""
	party = models.ForeignKey(Party, related_name="party_for_guest", default=1)
	guest = models.ForeignKey(Guest, related_name="guest", default=1)
	addedBy = models.ForeignKey(User, related_name="added_by", default=1)
	createdAt = models.DateTimeField(auto_now_add=True)
	signedIn = models.BooleanField(default=False)

	def __unicode__(self):
		return self.guest.name

	def __iter__(self):
		"""return a ** iterator of field,value"""
		for i in self._meta.get_all_field_names():
			yield (i, getattr(self,i))

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "Party Guests"
		verbose_name = "Party Guest"

	def toJSON(self):
		data = {}
		data['party'] = getattr(self,'party')
		data['guest'] = getattr(self,'guest').toJSON()
		data['addedBy'] = getattr(self,'addedBy')
		data['signedIn'] = getattr(self,'signedIn')


class PartyJob(models.Model):
	"""
		Model to represent a job for a specific party
	"""
	party = models.ForeignKey(Party, related_name="party_for_job", default=1)
	job = models.CharField(max_length=100, blank=True)
	user = models.ForeignKey(User, related_name="user", default=1)

	def __unicode__(self):
		return self.job

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "Party Jobs"
		verbose_name = "Party Job"




class AddMaleGuestForm(forms.Form):
    name = forms.CharField(max_length=100)
