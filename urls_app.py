# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from rome_app import views
'''
'''

urlpatterns = patterns('',
	#index and static
	
	url(r'^about/', views.about, name='about'),
	url(r'^links/$', views.links, name='links'),
	
	#books, prints, and essays
	url(r'^book_(?P<book_pid>\d+)_(?P<page_num>\d+)_(?P<book_num_on_page>\d+)/$', views.thumbnail_viewer, name='thumbnail_viewer'),
	url(r'^page_(?P<book_pid>\d+)_(?P<page_pid>\d+)_(?P<page_num>\d+)_(?P<book_num_on_page>\d+)/$', views.page, name='page_viewer'),
	url(r'^sprint_(?P<print_pid>\d+)_(?P<page_num>\d+)_(?P<print_num_on_page>\d+)/$', views.specific_print, name='specific_print'),
	url(r'^books/$', views.books, name='books'),
	url(r'^books_(?P<page>\d+)/$', views.books, name='books_specific_result_page'),
	url(r'^prints_(?P<page>\d+)/$', views.prints, name='prints_specific_result_page'),
	url(r'^prints_(?P<sort_by>\w+)/$', views.prints, name='prints_sort_by_specified'),
	url(r'^essay_(?P<essay_auth>\w+)/$', views.specific_essay, name='specific_essay'),
	url(r'^essays/$', views.essays, name='essays'),
	url(r'^prints/$', views.prints, name='prints'),
	
	url(r'^$', views.index, name='index'),
	
	# url(r'^search/', views.search, name='search'),
	# url(r'^search(?P<essay_auth>\w+)/$', views.search_results, name='search_results'),
  )
