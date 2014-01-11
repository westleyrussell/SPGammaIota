from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

class Link(models.Model):
	"""
		Model for a single link that a person may submit
	"""

	poster = models.ForeignKey(User)
	date = models.DateField()
	title = models.CharField(max_length=50)
	url = models.URLField()
	timesAccessed = models.PositiveIntegerField(default=0)
	lastAccessed = models.DateField()
	likeCount = models.IntegerField(default=0)
	commentCount = models.PositiveIntegerField(default=0)
	promoted = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name = "Link"
		verbose_name_plural = "Links"

class Like(models.Model):
	"""
		Model for a single like of a link
	"""

	liker = models.ForeignKey(User)
	link = models.ForeignKey(Link)

class Comment(models.Model):
	"""
		Model for a comment on a link
	"""

	commentor = models.ForeignKey(User)
	date = models.DateTimeField()
	link = models.ForeignKey(Link)
	comment = models.TextField()

class CommentForm(ModelForm):
	"""
		Form for adding a comment
	"""
	comment = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = Comment
		exclude = ['commentor', 'date', 'link']

class LinkForm(ModelForm):
	"""
		Form for adding a link
	"""

	title = forms.CharField(max_length = 50)
	url = forms.URLField(max_length=200)

	class Meta:
		model = Link
		exclude = ['poster', 'date', 'timesAccessed', 'lastAccessed', 'likeCount', 'commentCount', 'promoted']