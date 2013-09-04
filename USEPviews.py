# -*- coding: utf-8 -*-

import json, logging, pprint
import requests, math
from django.conf import settings as settings_project
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from usep_app import settings_app, models, utility_code
from .models import Page  # static pages
import usep_app.search.views

log = logging.getLogger(__name__)


## dynamic pages
## Facets to be shown on each page should be defined here since it's extracted from the solr query

@cache_page( settings_app.COLLECTIONS_CACHE_SECONDS )
def collections( request ):
  """Displays list of collections by Region."""
  
  page_data = Page.objects.using(settings_app.DB).get(head_title="Collections")
  region_data = utility_code.makeRegionList()

  assert sorted(region_data.keys()) == [ u'region_codes', u'regions' ]  # string-list & object-list
  data_dict = {
    u'region_list': region_data[ u'regions' ],
    u'region_codes': region_data[ u'region_codes' ],
    u'head_title': page_data.head_title,
    u'page_title': page_data.page_title,
    }
  ## display
  format = request.GET.get( u'format', None )
  callback = request.GET.get( u'callback', None )
  if format == u'json':
    assert type(data_dict) == dict
    output = json.dumps( data_dict, sort_keys=True, indent=2 )
    if callback:
      output = u'%s(%s)' % ( callback, output )
    return HttpResponse( output, content_type = u'application/javascript; charset=utf-8' )
  else:
    data_dict[u'login_url'] = settings_app.LOGIN_URL
    return render( request, u'usep_templates/collectionS.html', data_dict )

def collection( request, collection ):
  """Displays list of inscriptions for given collection."""
  ## get collection members

  c = models.Collection()
  c.collection_raw_string = collection
  c.kochief.parse_query_string(request)

  log.debug( u'in collection(); c.collection_raw_string: %s' % c.collection_raw_string )
  c.parseCollectionRawString()
  log.debug( u'in collection(); c.region, %s; c.settlement, %s; c.institution, %s; c.repository, %s' % (
    c.collection_region,
    c.collection_settlement,
    c.collection_institution,
    c.collection_repository )
   )
  c.makeCollectionQ()  # assembles q part of solr url
  log.debug( u'c.solr_q: %s' % c.solr_q )

  c.getCollectionMemberDataFromSolr()  # calls solr
  c.kochief.get_facet_counts()
 # log.debug( u'c.collection_solr_output: %s' % c.collection_solr_output )
 # log.debug( u'c.collection_solr_data: %s' % c.collection_solr_data )
  c.updateMemberInfo( request.META[u'wsgi.url_scheme'], request.META[u'SERVER_NAME'] )
 # log.debug( u'c.enhanced_members_data: %s' % c.enhanced_members_data )
  json_dict = {
    u'collection_title': c.collection_raw_string,
    u'inscriptions': c.enhanced_members_data,
    u'total_count': len( c.enhanced_members_data),
  }
  template_dict = dict(
    c.kochief.context.items() +
    json_dict.items() +
    {
      u'head_title': c.page_object.head_title,
      u'page_title': c.page_object.page_title,
      u'search_base': reverse('collection_url', args=(collection,))
    }.items()
  )
  ## display
  format = request.GET.get( u'format', None )
  callback = request.GET.get( u'callback', None )
  if format == u'json':
 #   try:
    output = json.dumps( json_dict, sort_keys=True, indent=2 )
#    except e:

    if callback:
      output = u'%s(%s)' % ( callback, output )
    return HttpResponse( output, content_type = u'application/javascript; charset=utf-8' )
  else:
    return render( request, u'usep_templates/collectioN.html', template_dict )

def display_inscription2( request, inscription_id ):
  """new version; uses xslt to grab data and create display / TODO: pull out data for optional json response."""
  ## build info
  insc = models.Inscription2()
  insc.run_xslt( inscription_id )   # applies xslt to collection-xml
  insc.update_xslt_html()           # applies some string replacement on the transformed xml
  insc.extract_inscription_data()   # extracts inscription and bibl info from transformed xml to a dict
  # insc.build_data_dict()
  ## display
  data_dict = {
    u'inscription_url': u'%s://%s%s' % ( request.META[u'wsgi.url_scheme'], request.META[u'SERVER_NAME'], reverse(u'inscription_url', args=(inscription_id,)) ),
    u'inscription_id': inscription_id,
    u'xslt_html': insc.updated_xslt_html,       # for template
    u'transform_url': insc.full_transform_url,  # shown during dev
    u'attribute_info': insc.extracted_data[u'attributes'],
    u'bib_info': insc.extracted_data[u'bibl'],
    u'summary':insc.extracted_data[u'summary'],
    u'xml_source_url': insc.xml_url,
    u'image_url': u'%s/usep/images/inscriptions/%s.jpg' % ( settings_project.STATIC_URL, inscription_id )
    }
  ## display
  format = request.GET.get( u'format', None )
  callback = request.GET.get( u'callback', None )
  if format == u'json':
    output = json.dumps( data_dict, sort_keys=True, indent=2 )
    if callback:
      output = u'%s(%s)' % ( callback, output )
    return HttpResponse( output, content_type = u'application/javascript; charset=utf-8' )
  else:
    return render( request, u'usep_templates/inscription2.html', data_dict )
  # return render( request, u'usep_templates/inscription2.html', data_dict )


# def display_inscription( request, inscription_id ):
#   """initial version; grabs data from solr"""
#   ## build info
#   insc = models.Inscription()
#   insc.getInscriptionData( inscription_id )  # makes solr call
#   insc.updateData()
#   log.debug( u'insc.inscription_solr_data, after update, is: %s' % insc.inscription_solr_data )
#   data_dict = {
#     u'id': inscription_id,
#     u'inscription_type': insc.inscription_solr_data[u'text_genre'],
#     u'object_type': insc.inscription_solr_data[u'object_type'],
#     u'bib_authors': insc.inscription_solr_data[u'bib_authors'],
#     u'bib_titles': sorted( insc.inscription_solr_data[u'bib_titles'] ),
#     u'condition': insc.inscription_solr_data[u'condition'],
#     u'decoration': insc.inscription_solr_data[u'decoration'],
#     u'language': insc.inscription_solr_data[u'language'],
#     u'material': insc.inscription_solr_data[u'material'],
#     u'msid_settlement': insc.inscription_solr_data[u'msid_settlement'],
#     u'msid_repository': insc.inscription_solr_data[u'msid_repository'],
#     u'msid_region': insc.inscription_solr_data[u'msid_region'],
#     u'msid_institution': insc.inscription_solr_data[u'msid_institution'],
#     u'msid_idno': insc.inscription_solr_data[u'msid_idno'],
#     u'writing': insc.inscription_solr_data[u'writing'],
#     u'xml_url': insc.xml_url,
#     u'image_url': insc.image_url,
#     }
#   ## display
#   format = request.GET.get( u'format', None )
#   callback = request.GET.get( u'callback', None )
#   if format == u'json':
#     output = json.dumps( data_dict, sort_keys=True, indent=2 )
#     if callback:
#       output = u'%s(%s)' % ( callback, output )
#     return HttpResponse( output, content_type = u'application/javascript; charset=utf-8' )
#   else:
#     return render( request, u'usep_templates/inscription.html', data_dict )


def login( request ):
  from django.contrib import auth
  log.debug( u'login() starting' )
  log.debug( u'request.META is: %s' % request.META )
  forbidden_response = u'You are not authorized to use the admin. If you believe you should be, please contact %s .' % settings_app.PERMITTED_ADMIN_CONTACT
  if u'Shibboleth-eppn' in request.META and request.META[ u'Shibboleth-eppn' ] in settings_app.PERMITTED_ADMINS:
    log.debug( u'shib-eppn found & is a permitted-admin' )
    name = request.META[ u'Shibboleth-eppn' ]
  elif settings_app.SPOOFED_ADMIN in settings_app.PERMITTED_ADMINS:
    log.debug( u'spoofed-admin is a permitted-admin' )
    name = settings_app.SPOOFED_ADMIN
  else:
    log.debug( u'not a legit url access; returning forbidden' )
    return HttpResponseForbidden( forbidden_response )
  try:  # authZ successful
    log.debug( u'trying user-object access' )
    user = auth.models.User.objects.using(settings_app.DB).get( username=name )
    user.backend = u'django.contrib.auth.backends.ModelBackend'
    auth.login( request, user )
    log.debug( u'user-object obtained & logged-in' )
    return HttpResponseRedirect( u'../../admin/usep_app/' )
  except Exception, e:  # could auto-add user
    log.debug( u'error: %s' % repr(e).decode(u'utf-8', u'replace') )
    return HttpResponseForbidden( forbidden_response )

@csrf_protect
#faceted publications view
def publications( request ):
  ## build info
  pubs = models.Publications()
  pubs.kochief.parse_query_string(request)

  pubs.getPubData()  # makes solr call
  pubs.buildPubLists()

  pubs.kochief.get_facet_counts()

  json_dict = {
    u'master_dict': pubs.master_pub_dict,
    u'corpora_list': pubs.corpora,
    u'journals_list': pubs.journals,
    u'monographs_list': pubs.monographs,
    u'total_count': len(pubs.master_pub_dict),
  }

  template_dict = dict(
    pubs.kochief.context.items() +
    json_dict.items() +
    {
      u'head_title': pubs.page_object.head_title,
      u'page_title': pubs.page_object.page_title,
      u'search_base': reverse('publications_url')
    }.items()
  )
  del template_dict['pagination']
  ## store inscription_ids for each publication to session for pubChildren()
  request.session['publications_to_inscription_ids_dict'] = json_dict['master_dict']
  ## display
  format = request.GET.get( u'format', None )
  callback = request.GET.get( u'callback', None )

  if format == u'json':
    output = json.dumps( json_dict, sort_keys=True, indent=2 )
    if callback:
      output = u'%s(%s)' % ( callback, output )
    return HttpResponse( output, content_type = u'application/javascript; charset=utf-8' )
  else:
    return render( request, u'usep_templates/publicationS.html',template_dict )

@csrf_protect
def pubChildren( request, publication):
  """displays listing of inscriptions for publication"""

  log.debug( u'publication: %s' % publication )
  assert type( publication ) == unicode

  if not u'publications_to_inscription_ids_dict' in request.session:
    pubs = models.Publications()
    pubs.getPubData()  # makes solr call
    pubs.buildPubLists()
    request.session['publications_to_inscription_ids_dict'] = pubs.master_pub_dict  # key: publication; value: list of inscription_ids
  data = request.session[u'publications_to_inscription_ids_dict'][publication]
  log.debug( u'publication data: %s' % data )
  pub = models.Publication()
  pub.kochief.parse_query_string(request)
  pub.getPubData( data )
  pub.kochief.get_facet_counts()
  pub.buildInscriptionList( request.META[u'wsgi.url_scheme'], request.META[u'SERVER_NAME'] )
  pub.makeImageUrls()
  json_dict = {
    u'publication_title': publication,
    u'inscriptions': pub.inscription_entries,
    u'total_count': int(pub.inscription_count),
  }
  template_dict = dict(
    json_dict.items() + 
    pub.kochief.context.items() + {
      u'head_title': pub.page_object.head_title,
      u'page_title': pub.page_object.page_title,
      u'search_base': reverse(u'publication_url', args=(publication,))
    }.items()
  )
  ## respond
  format = request.GET.get( u'format', None )
  callback = request.GET.get( u'callback', None )
  if format == u'json':
    output = json.dumps( json_dict[u'inscriptions'], sort_keys=True, indent=2 )
    if callback:
      output = u'%s(%s)' % ( callback, output )
    return HttpResponse( output, content_type = u'application/javascript; charset=utf-8' )
  else:
    return render( request, u'usep_templates/publicatioN.html', template_dict )

## static pages
def static( request, title ):
  page_data = Page.objects.using(settings_app.DB).get(head_title=title)
  page_dict = {
    u'head_title': page_data.head_title,
    u'page_title': page_data.page_title,
    u'content': page_data.content,
  }
  return render( request, u'usep_templates/static.html', page_dict )
  # return render_to_response( u'usep_templates/static.html', page_dict )
