# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Biography, Essay, Genre, Role
from .forms import BiographyModelForm, EssayModelForm

class BiographyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'trp_id', 'external_id']
    form = BiographyModelForm

class EssayAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title']
    form = EssayModelForm

class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'external_id']

class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'external_id']

admin.site.register(Biography, BiographyAdmin)
admin.site.register(Essay, EssayAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Role, GenreAdmin)

