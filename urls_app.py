# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns
from rome_app import views

'''
Ben, I took the sections below from: <http://www.stg.brown.edu:8080/exist/rome/index.html>.
I think there's a newer grey site. Feel free to change _anything_; I just wanted to get a something up on worfdev.
-ß

Thanks!
'''

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^about/',views.about, name='about'),
	url(r'^book_(?P<book_pid>\d+)_(?P<page_num>\d+)_(?P<book_num_on_page>\d+)/$', views.thumbnail_viewer, name='thumbnail_viewer'),
	url(r'^page_(?P<book_pid>\d+)_(?P<page_pid>\d+)_(?P<page_num>\d+)_(?P<book_num_on_page>\d+)/$', views.page, name='page_viewer'),
	url(r'^sprint_(?P<print_pid>\d+)_(?P<page_num>\d+)_(?P<print_num_on_page>\d+)/$', views.specific_print, name='specific_print'),
	url(r'^books/',views.books, name='books'),
	url(r'^books_(?P<page>\d+)/$', views.books, name='books_specific_result_page'),
	url(r'^prints_(?P<page>\d+)/$', views.prints, name='prints_specific_result_page'),
	url(r'^essay_(?P<essay_auth>\w+)/$', views.specific_essay, name='specific_essay'),
	url(r'^essays/',views.essays, name='essays'),
	url(r'^links/',views.links, name='links'),
	url(r'^prints/',views.prints, name='prints'),
	url(r'^search/',views.search, name='search'),
	url(r'^search(?P<essay_auth>\w+)/$', views.search_results, name='search_results'),
  # ( r'^books/$',  'rome_app.views.books' ),
  #   ( r'^prints/$',  'rome_app.views.prints' ),
  #   ( r'^people/$',  'rome_app.views.stub' ),
  #   ( r'^printshop/$',  'rome_app.views.stub' ),
  #   ( r'^network/$',  'rome_app.views.stub' ),
  #   ( r'^essays/$',  'rome_app.views.essays' ),
  #   ( r'^search/$',  'rome_app.views.stub' ),
  #   ( r'^links/$',  'rome_app.views.links' ),
  #   ( r'^about/$',  'rome_app.views.about' ),
  #   ( r'^$', 'rome_app.views.index' ),
  )
