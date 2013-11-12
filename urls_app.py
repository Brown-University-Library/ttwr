# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from rome_app import views
from django.contrib import admin


urlpatterns = patterns('',
    #admin
    url(r'^admin/', include(admin.site.urls), name='admin'),
    
    #index and static
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^links/$', views.links, name='links'),
    
    #books, prints, and essays
    url(r'^books/$', views.books, name='books'),
    url(r'^books/(?P<book_pid>\d+)/$', views.thumbnail_viewer, name='thumbnail_viewer'),
    url(r'^page_(?P<book_pid>\d+)_(?P<page_pid>\d+)_(?P<page_num>\d+)_(?P<book_num_on_page>\d+)/$', views.page, name='page_viewer'),
    url(r'^prints/$', views.prints, name='prints'),
    url(r'^prints_(?P<page>\d+)/$', views.prints, name='prints_specific_result_page'),
    url(r'^prints_(?P<sort_by>\w+)/$', views.prints, name='prints_sort_by_specified'),
    url(r'^sprint_(?P<print_pid>\d+)_(?P<page_num>\d+)_(?P<print_num_on_page>\d+)/$', views.specific_print, name='specific_print'),
    url(r'^essays/$', views.essays, name='essays'),
    url(r'^essay_(?P<essay_auth>\w+)/$', views.specific_essay, name='specific_essay'),
    url(r'^people/$', views.people, name='people'),
    url(r'^people/(?P<trp_id>\d+)/$', views.person_detail, name='person_detail'),
    url(r'^people/(?P<trp_id>\d+)/TEI/$', views.person_detail_tei, name='person_detail_tei'),
)
