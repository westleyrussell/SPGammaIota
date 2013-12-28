from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
import re

class Test(models.Model):
	"""
		Model for a test in the test bank.
	"""

	def __unicode__(self):
		return str(self.course) + ": " + str(self.name)

	#TODO clean any other inputs for convenience
	#TODO validate all inputs
		# Check that course has valid subject, and then 4 numbers?

	def clean(self):
		# Strip all non alpha-numeric characters from the class name
		if self.course:
			self.course = self.course.strip()
			self.course = re.sub(r'\W+', '', self.course)

	def validate_year(year):
		# Require four character long year
		if len(str(year)) != 4:
			raise ValidationError(u'Year must be four characters long.')

	# def validate_term(term):
		# if not term in ["A", "B", "C", "D", "E"]:
			# raise ValidationError(u'You must select a term.')

	professor = models.CharField(max_length=100)
	name = models.CharField(max_length=200)
	owner = models.CharField(max_length=100)
	course = models.CharField(max_length=100)
	year = models.IntegerField(default=date.today().year, validators=[validate_year])
	term = models.CharField(max_length=1, default='Click or type to select a term...', choices = (   ('', 'Click or type to select a term...'), \
																					('A','A Term'), \
																					('B','B Term'), \
																					('C','C Term'), \
																					('D','D Term'), \
																					('E','E Term')))
	docfile = models.FileField(upload_to='library')

