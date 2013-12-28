# -*- coding: utf-8 -*-
from django import forms
from models import Test

class DocumentForm(forms.ModelForm):

	class Meta:
		model = Test
		fields = ['name', 'owner', 'course', 'year', 'term', 'docfile', 'professor']
		widgets = {
			'name': forms.TextInput(attrs={'placeholder': 'Midterm, Final, etc.'}),
			'course': forms.TextInput(attrs={'placeholder': 'ECE2010, MA1024, etc.'}),
			'owner': forms.TextInput(attrs={'placeholder': 'First and last name...'}),
			'professor': forms.TextInput(attrs={'placeholder': 'First and last name...'}),
			'year': forms.TextInput(attrs={'placeholder': 'Four digit year...'}),
			'term': forms.Select(),
			'docfile': forms.FileInput(attrs={'class': 'ui input fluid active button'}),
		}
