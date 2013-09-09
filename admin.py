# -*- coding: utf-8 -*-

# from rome_app.models import AboutPage
from rome_app.models import About
from django.contrib import admin
import rome_app.admin


# class AboutAdmin(admin.ModelAdmin):
# 	fieldsets = (
# 		(None, {'fields': 'description'})
# 	)

# admin.site.register( AboutPage )

admin.site.register(About)