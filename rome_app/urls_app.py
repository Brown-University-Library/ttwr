from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import LoginView
from rome_app import views


BDR_ID_RE = '[a-z0-9]+'


urlpatterns = [
    #admin/user
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(template_name='rome_templates/login.html'), name='rome_login'),

    #index and static
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^links/$', views.links, name='links'),
    url(r'^shops/$', views.shops, name='shops'),

    #books, prints, essays, shops...
    url(r'^books/$', views.book_list, name='books'),
    url(fr'^books/(?P<book_id>{BDR_ID_RE})/$', views.book_detail, name='thumbnail_viewer'),
    url(fr'^books/(?P<book_id>{BDR_ID_RE})/(?P<page_id>{BDR_ID_RE})/$', views.page_detail, name='book_page_viewer'),
    url(fr'^books/(?P<book_id>{BDR_ID_RE})/(?P<page_id>{BDR_ID_RE})/annotations/new/$', views.new_annotation, name='new_annotation'),
    url(fr'^books/(?P<book_id>{BDR_ID_RE})/(?P<page_id>{BDR_ID_RE})/annotations/(?P<anno_id>{BDR_ID_RE})/edit/$', views.edit_annotation, name='edit_annotation'),
    url(r'^prints/$', views.print_list, name='prints'),
    url(fr'^prints/(?P<print_id>{BDR_ID_RE})/$', views.print_detail, name='specific_print'),
    url(fr'^prints/(?P<print_id>{BDR_ID_RE})/annotations/new/$', views.new_print_annotation, name='new_print_annotation'),
    url(fr'^prints/(?P<print_id>{BDR_ID_RE})/annotations/(?P<anno_id>{BDR_ID_RE})/edit/$', views.edit_print_annotation, name='edit_print_annotation'),
    url(r'^essays/$', views.essay_list, name='essays'),
    url(r'^essays/(?P<essay_slug>[\w-]+)/$', views.essay_detail, name='specific_essay'),
    url(r'^people/$', views.biography_list, name='people'),
    url(r'^people/(?P<trp_id>\d+)/$', views.biography_detail, name='person_detail'),
    url(r'^shop_list/$', views.shop_list, name='shop_list'),
    url(r'^shop_list/(?P<shop_slug>[\w-]+)/$', views.shop_detail, name='specific_shop'),
    url(r'^documents/$', views.documents, name='documents'),
    url(r'^documents/(?P<document_slug>[\w-]+)/$', views.document_detail, name='specific_document'),


    #create new records
    url(r'^genres/new/$', views.new_genre, name='new_genre'),
    url(r'^roles/new/$', views.new_role, name='new_role'),
    url(r'^biographies/new/$', views.new_biography, name='new_biography'),

    url(r'^search/$', views.search_page, name= 'search_page'),
]

