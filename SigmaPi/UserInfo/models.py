from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
	user = models.OneToOneField(User)
	picture = models.ImageField()
	phoneNumber = models.PositiveIntegerField()
	graduationYear = models.PositiveIntegerField()
	major = models.CharField(max_length=None)
	hometown = models.CharField(max_length=None)
	activities = models.CharField(max_length=None)
	interests = models.CharField(max_length=None)
	favoriteMemory = models.CharField(max_length=None)
	bigBrother = models.CharField(max_length=None)

	def __unicode__(self):
		return "Info for " + __unicode__(self.user)