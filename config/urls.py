from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
  url( r'^',  include('rome_app.urls_app') ),
]
