from django.db import models
import datetime

#Utility function to add a timestamp to uploaded files.
def timeStamped(fname, fmt='%Y-%m-%d_{fname}'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)


#Model to represent a single bylaw.
class Bylaws(models.Model):

	def bylawspath(self, filename):
		return "protected/bylaws/" + timeStamped(filename)

	date = models.DateField()
	filepath = models.FileField(upload_to=bylawspath)

	def __unicode__(self):
		return self.date.__str__()

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "Bylaws"
		verbose_name = "Bylaws"

#Model to represent a single house rule.
class HouseRule(models.Model):

	title = models.CharField(max_length=100)
	content = models.TextField()
	path = models.SlugField(max_length=15)

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "House Rules"
		verbose_name = "House Rule"

#Model for meeting minutes that are kept at all house meetings.
class MeetingMinutes(models.Model):

	def minutespath(self, filename):
		return "protected/minutes/" + timeStamped(filename)

	date = models.DateField()
	filepath = models.FileField(upload_to=minutespath)

	def __unicode__(self):
		return self.date.__str__()

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "Meeting Minutes"
		verbose_name = "Meeting Minutes"


#Model for guides that will be posted to the site, 
#including House Jobs and Party Jobs
class Guide(models.Model):

	def guidepath(self, filename):
		return "protected/guides/" + timeStamped(filename)

	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	filepath = models.FileField(upload_to=guidepath)
	path = models.SlugField(max_length=15)


	def __unicode__(self):
		return self.name