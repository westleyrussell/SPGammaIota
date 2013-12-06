from django.forms import ModelForm
from PartyList.models import Guest, PartyGuest
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
