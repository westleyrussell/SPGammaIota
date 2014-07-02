from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE

class BlogPost(models.Model):
	"""
		Model for blog post and content updates to be seen on the front page
	"""

	def blogpath(self, filename):
		"""
			Defines the place where uploaded images will be uploaded for the blogs
		"""
		return "blogs/" + filename

	poster = models.ForeignKey(User)
	date = models.DateField(auto_now=True)
	title = models.CharField(max_length=50)
	path = models.SlugField(max_length=12)
	content = models.TextField()
	image = models.FileField(upload_to=blogpath, blank=True, null=True)

	def __unicode__(self):
		"""
			Basically a tostring method
		"""
		return self.title

	def __str__(self):
		"""
			Basically a tostring method
		"""
		return self.title

	class Meta:
		verbose_name = "Blog Post"
		verbose_name_plural = "Blog Posts"


class BlogPostForm(ModelForm):
	"""
		Form for adding a blog post.
	"""
	title = forms.CharField(max_length=50)
	content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
	image = forms.FileField()

	class Meta:
		model = BlogPost
		exclude = ['poster', 'date', 'path']
