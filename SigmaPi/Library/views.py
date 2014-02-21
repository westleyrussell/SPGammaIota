# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from sendfile import sendfile

from models import Test, Textbook
from forms import DocumentForm, AddTextbookForm

def download_testscan(request, scan_index):
	scan = Test.objects.get(pk=scan_index)
	return sendfile(request, scan.docfile.path, attachment=True)


@login_required
def main(request):

	# Handle file upload
	if request.method == 'POST':

		test_form = DocumentForm(request.POST, request.FILES)
		if test_form.is_valid():
			test_form.save()
			messages.success(request, 'The test was uploaded. Thank you!')

			return HttpResponseRedirect(reverse('Library.views.main'))

		textbook_form = AddTextbookForm(request.POST)
		if textbook_form.is_valid():
			textbook_form.save()
			messages.success(request, 'The record was uploaded. Thank you!')

			return HttpResponseRedirect(reverse('Library.views.main'))


	else:
		test_form = DocumentForm() # A empty, unbound form
		textbook_form = AddTextbookForm() # A empty, unbound form

	tests = Test.objects.all()
	textbooks = Textbook.objects.all()

	# Render list page with the documents and the form
	return render_to_response(
		'library.html',
		{
			'tests': tests,
			'test_form': test_form,
		    'textbooks': textbooks,
		    'textbook_form': textbook_form
		},
		context_instance=RequestContext(request)
	)
