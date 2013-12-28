# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import Test
from forms import DocumentForm

@login_required
def main(request):
	# Handle file upload
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'The test was uploaded. Thank you!')

			# Redirect to the document list after POST
			return HttpResponseRedirect(reverse('Library.views.main'))
	else:
		form = DocumentForm() # A empty, unbound form

	# Load documents for the list page
	tests = Test.objects.all()

	# Render list page with the documents and the form
	return render_to_response(
		'library.html',
		{'tests': tests, 'form': form},
		context_instance=RequestContext(request)
	)
