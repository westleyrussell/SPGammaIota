from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Status(models.Model):
	status = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.status