from django.contrib import admin
from .models import Biography, Essay, Genre, Role, Static, Shop
from .forms import AdminBiographyForm, EssayModelForm, StaticModelForm

class BiographyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'trp_id', 'external_id']
    form = AdminBiographyForm

class EssayAdmin(admin.ModelAdmin):
    list_display = ['is_note', 'id', 'author', 'title']
    form = EssayModelForm

class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'external_id']

class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'external_id']

class StaticAdmin(admin.ModelAdmin):
	list_display = ['title', 'text']
	form = StaticModelForm

class ShopAdmin(admin.ModelAdmin):
	list_display = ['title', 'text']

admin.site.register(Biography, BiographyAdmin)
admin.site.register(Essay, EssayAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Role, GenreAdmin)
admin.site.register(Static, StaticAdmin)
admin.site.register(Shop, ShopAdmin)