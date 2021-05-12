from django.urls import include, re_path
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
  re_path( r'^',  include('rome_app.urls_app') ),
]
