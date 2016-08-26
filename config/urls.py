from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
  url( r'^rome/',  include('rome_app.urls_app') ),
  url( r'^admin/',  include(admin.site.urls) ),
]
