from django.forms import ModelForm
from PartyList.models import Guest, PartyGuest, Party
from django import forms
import datetime


class GuestForm(ModelForm):
	"""a form for adding a guest on the client."""
	name = forms.CharField(max_length=100)
	gender = forms.CharField(max_length=10)

	class Meta:
		model = Guest
		fields = ['name','gender']

	def __init__(self,*args, **kwargs):
		super(GuestForm,self).__init__(*args, **kwargs)
		#do extra stuff here if necessary

class PartyForm(ModelForm):
	"""a form for adding a guest on the client."""
	name = forms.CharField(max_length=100)
	date = forms.DateField()

	class Meta:
		model = Party
		fields = ['name','date']

	def __init__(self,*args, **kwargs):
		super(PartyForm,self).__init__(*args, **kwargs)
		#do extra stuff here if necessary

class EditPartyInfoForm(ModelForm):
	"""
		Form for editing a party
	"""
	name = forms.CharField(max_length=100)
	date = forms.DateField()
	jobs = forms.FileField(required=False)

	class Meta:
		model = Party
		fields = ['name','date','jobs']

	def __init__(self,*args, **kwargs):
		super(EditPartyInfoForm,self).__init__(*args, **kwargs)
		#do extra stuff here if necessary

class List():
	"""a class that holds a list of partyguests (of a specific gender)
	has some book keeping information. This makes it easier to display 
	and organize guests in the template"""

	def __init__(self,gender):
		self.gender = gender
		self.guests = []
		self.signed_in = -1


	def size(self):
		if self.signed_in >= 0:
			return self.signed_in
		else:
			return len(self.guests)
