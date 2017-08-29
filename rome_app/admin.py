# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Biography, Essay, Genre, Role, Static
from .forms import AdminBiographyForm, EssayModelForm

class BiographyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'trp_id', 'external_id']
    form = AdminBiographyForm

class EssayAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'is_note']
    form = EssayModelForm

class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'external_id']

class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'external_id']

class StaticAdmin(admin.ModelAdmin):
	list_display = ['title', 'text']

admin.site.register(Biography, BiographyAdmin)
admin.site.register(Essay, EssayAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Role, GenreAdmin)
admin.site.register(Static, StaticAdmin)
