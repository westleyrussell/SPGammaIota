from django.db import models
from django.contrib.auth.models import User

class Party(models.Model):
	"""
		Model to represent a party.
	"""
	name = models.CharField(max_length=100)
	date = models.DateField()

	def __unicode__(self):
		return self.name

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "Parties"
		verbose_name = "Party"

class Guest(models.Model):
	"""
		Model to represent a party guest
	"""
	name = models.CharField(max_length=100)
	birthDate = models.DateField()
	gender = models.CharField(max_length=100, blank=True)
	cardID = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		return self.name

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "Guests"
		verbose_name = "Guest"

class PartyGuest(models.Model):
	""" 
		Model to represent a guest for a specific party.
	"""
	party = models.ForeignKey(Party, related_name="party_for_guest", default=1)
	guest = models.ForeignKey(Guest, related_name="guest", default=1)
	addedBy = models.ForeignKey(User, related_name="added_by", default=1)

	def __unicode__(self):
		return self.guest.name

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "Party Guests"
		verbose_name = "Party Guest"

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