from django.db import models
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

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
	phoneNumber = models.CharField(default="555-555-5555", max_length=100)
	graduationYear = models.PositiveIntegerField(default=2015)
	classYear = models.CharField(default="Lambda", max_length=20)
	major = models.CharField(max_length=100, blank=True)
	hometown = models.CharField(max_length=100, blank=True)
	activities = models.TextField(blank=True)
	interests = models.TextField(blank=True)
	favoriteMemory = models.TextField(blank=True)
	bigBrother = models.ForeignKey(User, related_name="big_brother", default=1)

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
	phoneNumber = forms.IntegerField(required=False)
	major = forms.CharField(max_length=100, required=False)
	hometown = forms.CharField(max_length=100, required=False)
	activities = forms.CharField(widget=forms.Textarea, required=False)
	interests = forms.CharField(widget=forms.Textarea, required=False)
	favoriteMemory = forms.CharField(widget=forms.Textarea, required=False)

	class Meta:
		model = UserInfo
		exclude = ['picture', 'graduationYear', 'classYear', 'user', 'bigBrother']