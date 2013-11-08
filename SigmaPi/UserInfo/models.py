from django.db import models
from django.contrib.auth.models import User

def filepath(self, filename):
	return ""

# Create your models here.
class UserInfo(models.Model):
	user = models.OneToOneField(User)
	picture = models.FileField(upload_to=filepath, blank=True)
	phoneNumber = models.PositiveIntegerField(blank=True)
	graduationYear = models.PositiveIntegerField(blank=True)
	major = models.CharField(max_length=100, blank=True)
	hometown = models.CharField(max_length=100, blank=True)
	activities = models.CharField(max_length=200, blank=True)
	interests = models.CharField(max_length=200, blank=True)
	favoriteMemory = models.CharField(max_length=200, blank=True)
	bigBrother = models.ForeignKey(User, related_name="big_brother", blank=True)

	def __unicode__(self):
		return "Info for " + __unicode__(self.user)