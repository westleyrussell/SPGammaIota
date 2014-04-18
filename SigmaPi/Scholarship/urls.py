from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',

    # Viewing pages
	url(r'^$', 'Scholarship.views.index'),
	url(r'^study_hours/$', 'Scholarship.views.study_hours'),
	url(r'^tests/$', 'Scholarship.views.tests'),
	url(r'^textbooks/$', 'Scholarship.views.textbooks'),

	# Actions to POST to
	url(r'^study_hours/update_requirements/$', 'Scholarship.views.update_requirements'),
	url(r'^study_hours/record_hours/$', 'Scholarship.views.record_hours'),
	url(r'^tests/upload_test/$', 'Scholarship.views.upload_test'),

	# url(r'^update/$', 'Scholarship.views.update_user'),
	# url(r'^record/$', 'Scholarship.views.record_hours'),

	# Bylaws
	# url(r'^bylaws/$', 'Archives.views.bylaws'),
	# url(r'^bylaws/(?P<bylaw>[\d]+)/$', 'Archives.views.download_bylaw'),
	# url(r'^bylaws/delete/$', 'Archives.views.delete_bylaw'),

	# Meeting minutes
	# url(r'^minutes/$', 'Archives.views.minutes'),
	# url(r'^minutes/delete/$', 'Archives.views.delete_minutes'),
	# url(r'^minutes/(?P<minutes>[\d]+)/$', 'Archives.views.download_minutes'),

	# House guides
	# url(r'^guides/$', 'Archives.views.guides'),
	# url(r'^guides/delete/$', 'Archives.views.delete_guide'),
	# url(r'^guides/(?P<guides>[\d]+)/$', 'Archives.views.download_guides'),

	# House rules
	# url(r'^rules/$', 'Archives.views.rules'),
	# url(r'^rules/delete/$', 'Archives.views.delete_rules'),
	# url(r'^rules/(?P<rules>[\d]+)/$', 'Archives.views.download_rules'),
)

