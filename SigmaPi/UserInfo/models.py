from django.db import models
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

class PledgeClass(models.Model):
	"""
		Model for user pledge class relationship.
	"""

	name = models.CharField(max_length=100, default="Lambda")
	dateInitiated = models.DateField(blank=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Pledge Classes"
		verbose_name = "Pledge Class"

class UserInfo(models.Model):
	"""
		Model for site-specific user info.
		Complements the built in User models
	"""
	def filepath(self, filename):
		"""
			Defines where files uploaded by the user should be stored
		"""
		return "users/" + self.user.username + "/" + filename

	user = models.OneToOneField(User)
	picture = models.FileField(upload_to=filepath, null=True)
	phoneNumber = models.CharField(default="", max_length=100, blank=True)
	graduationYear = models.PositiveIntegerField(default=2015)
	classYear = models.CharField(default="Lambda", max_length=20, blank=True)
	major = models.CharField(max_length=100, blank=True)
	hometown = models.CharField(max_length=100, blank=True)
	activities = models.TextField(blank=True)
	interests = models.TextField(blank=True)
	favoriteMemory = models.TextField(blank=True)
	bigBrother = models.ForeignKey(User, related_name="big_brother", default=1)
	pledgeClass = models.ForeignKey(PledgeClass)

	def __unicode__(self):
		return self.user.username

	class Meta:
		verbose_name_plural = "User Info"
		verbose_name = "User Info"
		permissions = (
			("manage_users", "Can manage users."),
			)


class EditUserInfoForm(ModelForm):
	"""
		Form for editing a user
	"""
	phoneNumber = forms.CharField(max_length=100, required=False)
	major = forms.CharField(max_length=100, required=False)
	hometown = forms.CharField(max_length=100, required=False)
	activities = forms.CharField(widget=forms.Textarea, required=False)
	interests = forms.CharField(widget=forms.Textarea, required=False)
	favoriteMemory = forms.CharField(widget=forms.Textarea, required=False)

	class Meta:
		model = UserInfo
		exclude = ['picture', 'graduationYear', 'classYear', 'user', 'bigBrother', 'pledgeClass']