# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Biography, Essay

class BiographyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'trp_id']

class EssayAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title']

admin.site.register(Biography, BiographyAdmin)
admin.site.register(Essay, EssayAdmin)

