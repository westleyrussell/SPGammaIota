from django.db import models
from django.contrib.auth.models import User

# Model for blog posts and updates
class BlogPost(models.Model):
	def blogpath(self, filename):
		return "blogs/" + filename
	poster = models.ForeignKey(User)
	date = models.DateField(auto_now=True)
	title = models.CharField(max_length=50)
	path = models.SlugField(max_length=12)
	content = models.TextField()
	image = models.FileField(upload_to=blogpath, blank=True, null=True)

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name = "Blog Post"
		verbose_name_plural = "Blog Posts"
