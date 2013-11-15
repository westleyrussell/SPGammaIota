from django.db import models
from django.contrib.auth.models import User

#Model to represent a party.
class Party(models.Model):

	name = models.CharField(max_length=100)
	date = models.DateField()

	def __unicode__(self):
		return self.name

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "Parties"
		verbose_name = "Party"

#Model to represent a party guest.
class Guest(models.Model):

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

#Model to represent a party attendee.
class PartyGuest(models.Model):

	party = models.ForeignKey(Party, related_name="party", default=1)
	guest = models.ForeignKey(Guest, related_name="guest", default=1)
	addedBy = models.ForeignKey(User, related_name="added_by", default=1)

	def __unicode__(self):
		return self.guest.name

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "Party Guests"
		verbose_name = "Party Guest"