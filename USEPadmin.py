# -*- coding: utf-8 -*-

from usep_app.models import Institution, Region, Repository, Page
from django.contrib import admin
import usep_app.search.admin


class InstitutionAdmin(admin.ModelAdmin):
  ordering = [ 'code' ]
  list_display = [ 'code', 'name', 'settlement_code', 'region_code' ]
  list_filter = [ 'name', 'settlement_code', 'region_code' ]
  search_fields = [ 'code', 'name' ]
  readonly_fields = [ 'code', 'settlement_code', 'region_code' ]
  
  
class RegionAdmin(admin.ModelAdmin):
  ordering = [ 'code' ]
  list_display = [ 'code', 'name' ]
  search_fields = [ 'code', 'name' ]
  readonly_fields = [ 'code' ]
  
  
class RepositoryAdmin(admin.ModelAdmin):
  ordering = [ 'code' ]
  list_display = [ 'code', 'name', 'institution_code', 'settlement_code', 'region_code' ]
  list_filter = [ 'code', 'name', 'institution_code', 'settlement_code', 'region_code' ]
  readonly_fields = [ 'code', 'institution_code', 'settlement_code', 'region_code' ]


admin.site.register( Institution, InstitutionAdmin )
admin.site.register( Region, RegionAdmin )
admin.site.register( Repository, RepositoryAdmin )

## static pages
admin.site.register( Page )
