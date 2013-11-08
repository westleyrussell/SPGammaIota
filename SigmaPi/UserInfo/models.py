from django.db import models
from django.contrib.auth.models import User

def filepath(self, filename):
	return ""

# Create your models here.
class UserInfo(models.Model):
	user = models.OneToOneField(User, required=false)
	picture = models.FileField(upload_to=filepath, required=false)
	phoneNumber = models.PositiveIntegerField(required=false)
	graduationYear = models.PositiveIntegerField(required=false)
	major = models.CharField(max_length=100, required=false)
	hometown = models.CharField(max_length=100, required=false)
	activities = models.CharField(max_length=200, required=false)
	interests = models.CharField(max_length=200, required=false)
	favoriteMemory = models.CharField(max_length=200, required=false)
	bigBrother = models.ForeignKey(User, related_name="big_brother", required=false)

	def __unicode__(self):
		return "Info for " + __unicode__(self.user)