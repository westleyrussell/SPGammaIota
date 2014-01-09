from django.db import models
import datetime

def timeStamped(fname, fmt='%Y-%m-%d_{fname}'):
	"""
		Utility function to add a timestamp to uploaded files.
	"""
	return datetime.datetime.now().strftime(fmt).format(fname=fname)


class Bylaws(models.Model):
	"""
		Model to represent a single bylaw.
	"""
	def bylawspath(self, filename):
		"""
			Defines where bylaws should be stored
		"""
		return "protected/bylaws/" + timeStamped(filename)

	date = models.DateField()
	filepath = models.FileField(upload_to=bylawspath)

	def __unicode__(self):
		return self.date.__str__()

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "Bylaws"
		verbose_name = "Bylaws"

class HouseRules(models.Model):
	"""
		Model to represent a house rule.
	"""
	def houserulespath(self, filename):
		"""
			Defines where house rules should be stored.
		"""
		return "protected/houserules/" + timeStamped(filename)
	date = models.DateField()
	filepath = models.FileField(upload_to=houserulespath)

	def __unicode__(self):
		return self.date.__str__()

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "House Rules"
		verbose_name = "House Rule"

class MeetingMinutes(models.Model):
	"""
		Model for meeting minutes that are kept at all house meetings.
	"""

	def minutespath(self, filename):
		"""
			Defines where minutes should be stored
		"""
		return "protected/minutes/" + timeStamped(filename)

	date = models.DateField()
	filepath = models.FileField(upload_to=minutespath)

	def __unicode__(self):
		return self.date.__str__()

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "Meeting Minutes"
		verbose_name = "Meeting Minutes"



class Guide(models.Model):
	"""
		Model for guides that will be posted to the site, 
		including House Jobs and Party Jobs
	"""

	def guidepath(self, filename):
		"""
			Defines where the guides should be uploaded/stored
		"""
		return "protected/guides/" + timeStamped(filename)

	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	filepath = models.FileField(upload_to=guidepath)
	path = models.SlugField(max_length=15)


	def __unicode__(self):
		return self.name