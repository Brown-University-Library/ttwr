from django.conf.urls import url
from django.contrib import admin
from django.urls import include, re_path

from config.middleware.turnstile_view import turnstile_verify

admin.autodiscover()

urlpatterns = [
    url(r'^turnstile-verify/', turnstile_verify, name='turnstile-verify'),  # turnstile verify endpoint
    re_path(r'^', include('rome_app.urls_app')),
]
