from django.db import models
from django.contrib.auth.models import User

def filepath(self, filename):
	return ""

# Create your models here.
class UserInfo(models.Model):
	user = models.OneToOneField(User)
	picture = models.FileField(upload_to=filepath)
	phoneNumber = models.PositiveIntegerField()
	graduationYear = models.PositiveIntegerField()
	major = models.CharField(max_length=100)
	hometown = models.CharField(max_length=100)
	activities = models.CharField(max_length=200)
	interests = models.CharField(max_length=200)
	favoriteMemory = models.CharField(max_length=200)
	bigBrother = models.ForeignKey(User, related_name="big_brother")

	def __unicode__(self):
		return "Info for " + __unicode__(self.user)