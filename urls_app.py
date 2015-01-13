# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login
from rome_app import views


urlpatterns = patterns('',
    #admin/user
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^login/$', login, {'template_name': 'rome_templates/login.html'}, name='rome_login'),

    #index and static
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^links/$', views.links, name='links'),

    #books, prints, and essays
    url(r'^books/$', views.book_list, name='books'),
    url(r'^books/(?P<book_id>\d+)/$', views.book_detail, name='thumbnail_viewer'),
    url(r'^books/(?P<book_id>\d+)/(?P<page_id>\d+)/$', views.page_detail, name='book_page_viewer'),
    url(r'^books/(?P<book_id>\d+)/(?P<page_id>\d+)/annotations/new/$', views.new_annotation, name='new_annotation'),
    url(r'^prints/$', views.print_list, name='prints'),
    url(r'^prints/(?P<print_id>\d+)/$', views.print_detail, name='specific_print'),
    url(r'^essays/$', views.essay_list, name='essays'),
    url(r'^essays/(?P<essay_slug>\w+)/$', views.essay_detail, name='specific_essay'),
    url(r'^people/$', views.biography_list, name='people'),
    url(r'^people/(?P<trp_id>\d+)/$', views.biography_detail, name='person_detail'),
    url(r'^people/(?P<trp_id>\d+)/TEI/$', views.person_detail_tei, name='person_detail_tei'),

    url(r'^genres/new/$', views.new_genre, name='new_genre'),
    url(r'^roles/new/$', views.new_role, name='new_role'),
)
