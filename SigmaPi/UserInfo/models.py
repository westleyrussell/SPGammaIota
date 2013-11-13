from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
	def filepath(self, filename):
		return "users/" + self.user.username + "/" + filename

	user = models.OneToOneField(User)
	picture = models.FileField(upload_to=filepath, null=True)
	phoneNumber = models.PositiveIntegerField(default=5555555555)
	graduationYear = models.PositiveIntegerField(default=2015)
	major = models.CharField(max_length=100, blank=True)
	hometown = models.CharField(max_length=100, blank=True)
	activities = models.TextField(blank=True)
	interests = models.TextField(blank=True)
	favoriteMemory = models.TextField(blank=True)
	bigBrother = models.ForeignKey(User, related_name="big_brother", default=1)

	def __unicode__(self):
		return self.user.username

	#Setup meta info about this model
	class Meta:
		verbose_name_plural = "User Info"
		verbose_name = "User Info"