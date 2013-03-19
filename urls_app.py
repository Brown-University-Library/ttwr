# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns

'''
Ben, I took the sections below from: <http://www.stg.brown.edu:8080/exist/rome/index.html>.
I think there's a newer grey site. Feel free to change _anything_; I just wanted to get a something up on worfdev.
-ß
'''

urlpatterns = patterns('',
  ( r'^books/$',  'rome_app.views.stub' ),
  ( r'^prints/$',  'rome_app.views.stub' ),
  ( r'^people/$',  'rome_app.views.stub' ),
  ( r'^printshop/$',  'rome_app.views.stub' ),
  ( r'^network/$',  'rome_app.views.stub' ),
  ( r'^essays/$',  'rome_app.views.stub' ),
  ( r'^search/$',  'rome_app.views.stub' ),
  ( r'^links/$',  'rome_app.views.stub' ),
  ( r'^about/$',  'rome_app.views.stub' ),
  ( r'^$', 'rome_app.views.stub' ),
  )
