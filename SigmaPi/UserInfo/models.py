from django.db import models
from django.contrib.auth.models import User

def filepath(self, filename):
	return ""

# Create your models here.
class UserInfo(models.Model):
	user = models.OneToOneField(User)
	picture = models.FileField(upload_to=filepath, null=True)
	phoneNumber = models.PositiveIntegerField(default=5555555555)
	graduationYear = models.PositiveIntegerField(default=2015)
	major = models.CharField(max_length=100, blank=True)
	hometown = models.CharField(max_length=100, blank=True)
	activities = models.CharField(max_length=200, blank=True)
	interests = models.CharField(max_length=200, blank=True)
	favoriteMemory = models.CharField(max_length=200, blank=True)
	bigBrother = models.ForeignKey(User, related_name="big_brother", default=1)

	def __unicode__(self):
		return self.user.username