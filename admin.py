# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Biography, Essay
from .forms import BiographyModelForm, EssayModelForm

class BiographyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'trp_id', 'external_id']
    form = BiographyModelForm

class EssayAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title']
    form = EssayModelForm

admin.site.register(Biography, BiographyAdmin)
admin.site.register(Essay, EssayAdmin)

