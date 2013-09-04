# -*- coding: utf-8 -*-

import json, logging, os, pprint
import requests
from exceptions import TypeError
from requests.packages import urllib3
from django.conf import settings as settings_project
from django.core.urlresolvers import reverse
from django.db import models, connections, connection
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_unicode
from usep_app import settings_app
from usep_app.search.models import Facet, Kochief, SolrHelper

connection.text_factory = lambda x: unicode(x, "utf-8", "ignore")
log = logging.getLogger(__name__)

### collection classes ###

class Region(models.Model):
  code = models.CharField( blank=True, max_length=10, help_text=u'auto-populated' )
  name = models.CharField( blank=True, max_length=100 )

  def __unicode__(self):
    return smart_unicode( self.code, u'utf-8', u'replace' )

  def getSettlements( self ):
    self.settlements_solr_url = u''
    self.settlements_solr_response = u''
    self.settlements = []
    sh = SolrHelper( params = {
      u'q': u'msid_region:%s' % self.code,
      u'rows': u'0',
      u'facet.field': u'msid_settlement' }
      )
    self.settlements_solr_response, jdict = sh.query()
    self.settlements_solr_url = self.settlements_solr_response.url
    assert sorted(jdict.keys()) == [u'facet_counts', u'response', u'responseHeader'], sorted(jdict.keys())
    settlements_solr = jdict[u'facet_counts'][u'facet_fields'][u'msid_settlement']
    for ss in settlements_solr:  # settlements_a eg: [ u'Clev', 2, u'Cin', 1 ]
      if type(ss) == unicode:
        s = Settlement()
        s.source_name = ss
        s.region_source_name = self.code
        s.getInstitutions()
        log.debug( u'in Region.getSettlements(); s.institutions is: %s' % s.institutions )
        s.getRepositories()
        self.settlements.append( {
          u'source_name': s.source_name,
          u'region_source_name': s.region_source_name,
          u'institutions': s.institutions,
          u'institutions_count': len(s.institutions),
          u'settlement_repositories': s.settlement_repositories,
          u'repositories_count': len(s.settlement_repositories) }
          )
        self.settlements = sorted( self.settlements, key=lambda settlement: settlement[u'source_name'] )

  def getInstitutions( self ):
    """Builds institution list for DC region."""
    self.institutions = []
    if not self.code == u'DC':
      return
    ## get solr data
    sh = SolrHelper(params = {
      u'q': u'msid_region:%s' % self.code,
      u'rows': u'0',
      u'facet.field': u'msid_institution' }
      )
    r, jdict = sh.query()
    log.debug( u'in Region.getInstitutions(); r.url is: %s' % r.url )
    assert sorted(jdict.keys()) == [u'facet_counts', u'response', u'responseHeader'], sorted(jdict.keys())
    region_institutions = jdict[u'facet_counts'][u'facet_fields'][u'msid_institution']
    log.debug( u'in Region.getInstitutions(); region_institutions is: %s' % region_institutions )
    ## update institutions
    for entry in region_institutions:
      if type(entry) == unicode:
        try:
          i = Institution.objects.using(settings_app.DB).get( code=entry )
          log.debug( u'in Region.getInstitutions(); institution object found' )
        except Exception as e:
          log.debug( u'in Region.getInstitutions(); exception e is: %s' % repr(e).decode(u'utf-8', u'replace') )
          i = Institution()
          i.code = entry
          # i.settlement_code = u''  # not applicable
          i.region_code = self.code
          i.save(using=settings_app.DB)
          log.debug( u'in Region.getInstitutions(); new institution saved' )
        collection_id = u'%s.%s' % ( self.code, i.code )

        self.institutions.append( {
          u'code': i.code,
          u'name': i.name,
          u'description': i.description,
          u'address': i.address,
          u'url': i.url,
          u'repositories': [],
          u'collection_id': collection_id,
          u'collection_url': u'%s://%s%s' % (
            u'http',
            settings_app.SERVER_NAME,
            reverse( u'collection_url', args=(collection_id,) )
          )
        } )
    log.debug( u'in Region.getInstitutions(); self.institutions before sort is: %s' % self.institutions )
    self.institutions = sorted( self.institutions, key=lambda inst: inst[u'code'] )
    log.debug( u'in Settlement.getInstitutions(); self.institutions after sort is: %s' % self.institutions )
    return

  def getInscriptions( self ):
    """Builds inscription list for 'None' collection edge-case."""
    self.inscriptions = []
    if not self.code == u'No':
      return
    collection_id = self.code
    self.inscriptions.append( {
      u'collection_id': collection_id,
      u'collection_url': u'%s://%s%s' % (
          u'http',
          settings_app.SERVER_NAME,
          reverse( u'collection_url', args=(collection_id,) )
        )
      } )
    return

  # end class Region()


class Settlement(object):

  def __init__(self):
    self.source_name = None
    self.region_source_name = None  # the two-letter code
    self.institutions_solr_url = None
    self.institutions_solr_response = None
    self.institutions = []
    self.settlement_repositories = []  # MA.Glouc has no institutions, but a repository

  def getInstitutions( self ):
    """Builds institutions list."""
    sh = SolrHelper(params = {
      u'q': u'*:*',
      u'rows': u'0',
      u'fq': [
        u'msid_region:%s' % self.region_source_name,
        u'msid_settlement:%s' % self.source_name
        ],
      u'facet.field': u'msid_institution' }
    )
    r, jdict = sh.query()
    log.debug( u'getInstitution solr r.url: %s' % r.url )
    institutions_solr = jdict[u'facet_counts'][u'facet_fields'][u'msid_institution']
    for in_so in institutions_solr:
      if type(in_so) == unicode:
        log.debug( u'processing in_so: %s' % in_so )
        try:
          i = Institution.objects.using(settings_app.DB).get( code=in_so )
          log.debug( u'in Settlement.getInstitutions(); institution object found' )
          i.getRepositories()
          log.debug( u'in Settlement.getInstitutions(); i.repositories is: %s' % i.repositories )
        except Exception as e:
          log.debug( u'in Settlement.getInstitutions(); exception e is: %s' % repr(e).decode(u'utf-8', u'replace') )
          i = Institution()
          i.code = in_so
          i.settlement_code = self.source_name
          i.region_code = self.region_source_name
          i.getRepositories()
          log.debug( u'in Settlement.getInstitutions(); i.repositories_2 is: %s' % i.repositories )
          # if i.repositories == None:
          #   log.debug( u'in Settlement.getInstitutions(); i.repositories_2 is None' )
            # i.save()  # db is only for mapping, so only _save_ if necessary -- TODO: reenable save when appropriate after more testing
        if i.repositories:
          self.institutions.append( {
            u'code': i.code,
            u'name': i.name,
            u'description': i.description,
            u'address': i.address,
            u'url': i.url,
            u'repositories': i.repositories,
            u'collection_id': '',
            u'collection_url': u''
          } )
        else:
          collection_id = u'%s.%s.%s' % ( self.region_source_name, self.source_name, i.code )
          self.institutions.append( {
            u'code': i.code,
            u'name': i.name,
            u'description': i.description,
            u'address': i.address,
            u'url': i.url,
            u'repositories': i.repositories,
            u'collection_id': collection_id,
            u'collection_url': u'%s://%s%s' % (
              u'http',
            settings_app.SERVER_NAME,
            reverse( u'collection_url', args=(collection_id,) )
            )
          } )
    log.debug( u'in Settlement.getInstitutions(); self.institutions before sort is: %s' % self.institutions )
    self.institutions = sorted( self.institutions, key=lambda inst: inst[u'code'] )
    log.debug( u'in Settlement.getInstitutions(); self.institutions after sort is: %s' % self.institutions )
    return

  def getRepositories(self):
    """Builds repositories list for those repos that are at the settlement, not institution, level."""
    sh = SolrHelper( params = {
      u'q': u'*:*',
      u'rows': u'0',
      u'fq': [
        u'msid_region:%s' % self.region_source_name,
        u'msid_settlement:%s' % self.source_name
        ],
      u'facet.field': u'msid_repository' }
      )
    r, jdict = sh.query()
    log.debug( u'in Settlement.getRepositories(); solr r.url: %s' % r.url )
    log.debug( u'in Settlement.getRepositories(); repo_solr_response: %s' % r.content.decode( u'utf-8', u'replace' ) )
    solr_repositories = jdict[u'facet_counts'][u'facet_fields'][u'msid_repository']
    for solr_repo in solr_repositories:
      if type(solr_repo) == unicode:
        log.debug( u'in Settlement.getRepositories(); processing solr_repo: %s' % solr_repo )
        ## only handle IF NOT ALREADY IN INSTITUTIONS.REPOSITORIES!! ###
        inst_repo_check = u'not_found'
        for inst in self.institutions:
          for institutional_repo in inst[u'repositories']:
            if institutional_repo[u'code'] == solr_repo:
              inst_repo_check = u'found'
              break
          if inst_repo_check == u'found':
            break
        if inst_repo_check == u'not_found':
          log.debug( u'in Settlement.getRepositories(); solr_repo: not found institutions check' )
          try:
            r = Repository.objects.using(settings_app.DB).get( code=solr_repo )
          except Exception as e:
            log.debug( u'in Settlement.getRepositories(); exception e is: %s' % repr(e).decode(u'utf-8', u'replace') )
            r = Repository()
            r.code = solr_repo
            # TODO? -- populate other and save?
          self.settlement_repositories.append( {
            u'code': r.code,
            u'name': r.name,
            u'description': r.description,
            u'address': r.address,
            u'url': r.url,
            } )
    log.debug( u'in Settlement.getRepositories(); self.settlement_repositories before sort is: %s' % self.settlement_repositories )
    self.settlement_repositories = sorted( self.settlement_repositories, key=lambda repo: repo[u'code'] )
    log.debug( u'in Settlement.getRepositories(); self.settlement_repositories after sort is: %s' % self.settlement_repositories )

  # end class Settlement()

class Institution( models.Model ):
  code = models.CharField( blank=True, max_length=10, help_text=u'auto-populated' )
  settlement_code = models.CharField( blank=True, max_length=10, help_text=u'auto-populated' )
  region_code = models.CharField( blank=True, max_length=10, help_text=u'auto-populated' )
  name = models.CharField( blank=True, max_length=100 )
  address = models.CharField( blank=True, max_length=200, help_text=u'single string' )
  url = models.CharField( blank=True, max_length=200 )
  description = models.TextField( blank=True )

  def __unicode__(self):
    return smart_unicode( self.name, u'utf-8', u'replace' )

  def getRepositories( self ):
    self.repositories_solr_url = u''
    self.repositories_solr_response = u''
    self.repositories = []  # list of dicts
    sh = SolrHelper( params = {
      u'q': u'*:*',
      u'rows': u'0',
      u'fq': [
        u'msid_region:%s' % self.region_code,
        u'msid_settlement:%s' % self.settlement_code,
        u'msid_institution:%s' % self.code
        ],
      u'facet.field': u'msid_repository' }
    )
    r, jdict = sh.query()
    self.repositories_solr_url = r.url
    log.debug( u'in Institution.getRepositories(); self.repositories_solr_url is: %s' % self.repositories_solr_url )
    self.repositories_solr_response = r.content.decode( u'utf-8', u'replace' )
    log.debug( u'in Institution.getRepositories(); self.repositories_solr_response is: %s' % self.repositories_solr_response )

    repositories_solr = jdict[u'facet_counts'][u'facet_fields'][u'msid_repository']
    for re_so in repositories_solr:
      if type(re_so) == unicode:
        try:
          repo = Repository.objects.using(settings_app.DB).get( code=re_so, institution_code=self.code, settlement_code=self.settlement_code, region_code=self.region_code )
        except:
          repo = Repository()
          repo.code = re_so
          repo.institution_code = self.code
          repo.settlement_code = self.settlement_code
          repo.region_code = self.region_code
          # repo.save() # TODO -- REENABLE
        collection_id = u'%s.%s.%s.%s' % ( self.region_code, self.settlement_code, self.code, repo.code )
        self.repositories.append( {
          u'code': repo.code,
          u'name': repo.name,
          u'description': repo.description,
          u'address': repo.address,
          u'url': repo.url,
          u'collection_id': collection_id,
          u'collection_url': u'%s://%s%s' % (
            u'http',
            settings_app.SERVER_NAME,
            reverse( u'collection_url', args=(collection_id,) )
            )
          } )
        self.repositories = sorted( self.repositories, key=lambda repo: repo[u'code'] )
        log.debug( u'in Institution.getRepositories(); self.repositories for REG.SET.INS "%s.%s.%s" is: %s' % (self.region_code, self.settlement_code, self.code, self.repositories) )

  # end class Institution()


class Repository(models.Model):
  code = models.CharField( blank=True, max_length=10, help_text=u'auto-populated' )
  institution_code = models.CharField( blank=True, max_length=10, help_text=u'auto-populated' )
  settlement_code = models.CharField( blank=True, max_length=10, help_text=u'auto-populated' )
  region_code = models.CharField( blank=True, max_length=10, help_text=u'auto-populated' )
  name = models.CharField( blank=True, max_length=100 )
  address = models.CharField( blank=True, max_length=200, help_text=u'single string' )
  url = models.CharField( blank=True, max_length=200 )
  description = models.TextField( blank=True )
  inscription_count = 0

  def __unicode__(self):
    return smart_unicode( self.name, u'utf-8', u'replace' )

  class Meta:
    verbose_name_plural = u'Repositories'

  # end class Repository()

class Page(models.Model):
  head_title = models.CharField( blank=False, max_length=100, unique=True )
  page_title = models.CharField( blank=True, max_length=100 )
  content = models.TextField( blank=True, help_text='HTML allowed.' )
  facets = models.ManyToManyField(Facet, blank=True)
  def __unicode__(self):
    return smart_unicode( self.page_title, u'utf-8', u'replace' )
  class Meta:
    verbose_name_plural = u'Pages'

  def facet_params(self, fls):
    if not type(fls) == unicode and not type(fls) == str:
      raise TypeError, "facet_params must take a single argument that is a string or unicode sequence."
    params = {
      u'facet.field': [],
      u'fl': fls
    }
    for facet_option in self.facets.all():
      params[u'facet.field'].append(unicode(facet_option.field))
      if len(params['fl']) == 0:
        params['fl'] = unicode(facet_option.field)
      else:
        params['fl'] += u",%s" % facet_option.field
      if not facet_option.sort_by_count:
        params = dict(params.items() + { u'f.%s.facet.sort' % facet_option.field: False }.items())

    return params

### other non-db classes ###
class Collection(object):

  def __init__(self):
    self.collection_raw_string = None
    self.collection_region = None
    self.collection_settlement = None
    self.collection_institution = None
    self.collection_repository = None
    self.solr_q = None
    self.collection_solr_output = None
    self.collection_solr_data = None
    self.enhanced_members_data = None
    self.kochief = Kochief()
    try:
      self.page_object = Page.objects.using(settings_app.DB).get(head_title="Collection")
    except ObjectDoesNotExist:
      self.page_object = Page(head_title="Collection")
      self.page_object.save(using=settings_app.DB)

  def parseCollectionRawString(self):
    """Parses collection_string into components in preparation for creating solr query."""
    parts = self.collection_raw_string.split( u'.' )
    self.collection_region = parts[0]
    if self.collection_region == u'DC':  # edge-case
      self.collection_institution = parts[1]
    elif self.collection_region == u'No':  # edge-case
      return
    else:
      self.collection_settlement = parts[1]
      self.collection_institution = parts[2]
      try:
        self.collection_repository = parts[3]
      except IndexError:
        pass
    return

  def makeCollectionQ(self):
    '''
    Creates solr u'q' parameter.
    '''
    if self.collection_repository != None:
      s = u'msid_region:"%s" AND msid_settlement:"%s" AND msid_institution:"%s" AND msid_repository:"%s"' % (
        self.collection_region,
        self.collection_settlement,
        self.collection_institution,
        self.collection_repository
        )
    elif not self.collection_settlement:  # edge-case for region: 'No' (unknown)
      s = u'msid_region:"%s"' % self.collection_region
    else:
      s = u'msid_region:"%s" AND msid_settlement:"%s" AND msid_institution:"%s"' % (
        self.collection_region,
        self.collection_settlement,
        self.collection_institution,
        )
    self.solr_q = s
    log.debug( u'- solr_q is: %s' % self.solr_q )
    return

  def getCollectionMemberDataFromSolr(self):
    """
    Queries solr for collection info.
    If nothing found, revises query with self.collection_raw_string (handles, eg, Gloucestor, which has a repository at the Settlement level)
    """
  
    payload = {
      u'fl': u'id,status',
    }
    payload.update(self.page_object.facet_params(payload['fl']))
    self.kochief.get_params_from_query(self.solr_q)
    r, d = self.kochief.get_solr_response(payload)
    log.debug( u'in Collection.getCollectionMemberDataFromSolr(); Kochief call: %s' % d[u'responseHeader'][u'params'] )
    log.debug( u'in Collection.getCollectionMemberDataFromSolr(); single collection solr call: %s' % r.url )
    self.collection_solr_output = r.content.decode( u'utf-8', u'replace')
    self.collection_solr_data = d[u'response'][u'docs']
    if len( self.collection_solr_data ) == 0:
      r, d = self.kochief.get_solr_response(payload)
      log.debug( u'in Collection.getCollectionMemberDataFromSolr(); single collection solr call, SECOND TRY: %s' % r.url )
      self.collection_solr_output = r.content.decode( u'utf-8', u'replace')
      self.collection_solr_data = d[u'response'][u'docs']
    self.solr_count = d[u'response'][u'numFound'] - 1
    return

  def updateMemberInfo( self, url_scheme, server_name ):
    u"""Adds to dict entries from solr: image_url and item-url"""
    ## get list of inscription images
    inscription_images_dir = u'%s/usep/images/inscriptions/' % settings_project.STATIC_ROOT
    inscription_images = os.listdir( inscription_images_dir )
    new_list = []
    for entry in self.collection_solr_data:
      ## update image url
      if u'%s.jpg' % entry[u'id'] in inscription_images:
        entry[u'image_url'] = u'%s/usep/images/inscriptions/%s.jpg' % ( settings_project.STATIC_URL, entry[u'id'] )
      else:
        entry[u'image_url'] = None
      ## update item url
      entry[u'url'] = u'%s://%s%s' % ( url_scheme, server_name, reverse(u'inscription_url', args=(entry[u'id'],)) )
      new_list.append( entry )

    self.enhanced_members_data = new_list
    return

  # end class Collection()


class Inscription2(object):
  """Handles code to display the inscription page."""

  def __init__(self):
    self.inscription_id = None      # set by self.run_xslt(); used by self.updateXsltHtml()
    self.full_transform_url = None  # set by self.run_xslt(); used by views.display_inscription2()
    self.xslt_html = None           # set by self.run_xslt(); used by self.updateXsltHtml()
    self.updated_xslt_html = None   # set by self.run_xslt(); used by views.display_inscription2() & self.updateDataDict()
    self.xml_url = None             # set by self.run_xslt(); used by views.display_inscription2()
    self.extracted_data = None      # dict set by self.extract_inscription_data(); used by views.display_inscription2()

  def run_xslt( self, inscription_id ):
    """Applies stylesheet to xml record."""
    self.inscription_id = inscription_id
    self.xml_url = u'%s/%s.xml' % ( settings_app.TRANSFORMER_XML_URL_SEGMENT, self.inscription_id )
    self.full_transform_url = u'%s?source=%s&style=%s' % ( settings_app.TRANSFORMER_URL, self.xml_url, settings_app.TRANSFORMER_XSL_URL )
    log.debug( u'self.full_transform_url: %s' % self.full_transform_url )
    r = requests.get( self.full_transform_url )
    self.xslt_html = r.content.decode( u'utf-8', u'replace' )
    log.debug( u'self.xslt_html: %s' % self.xslt_html )
    return

  def update_xslt_html(self):
    """Updates transformation output."""
    ## image url
    search_string = u'<img src="../Pictures/Thumbnails/%s.jpg"/>' % self.inscription_id
    replace_string = u'<img src="%susep/images/inscriptions/%s.jpg"/>' % ( settings_project.STATIC_URL, self.inscription_id )
    self.updated_xslt_html = self.xslt_html.replace( search_string, replace_string )
    ## blank gif
    search_string = u'<img src="http://static.flowplayer.org/tools/img/blank.gif"/>'
    replace_string = u''
    self.updated_xslt_html = self.updated_xslt_html.replace( search_string, replace_string )
    ## xml link
    search_string = u'http://dev.stg.brown.edu/projects/usepigraphy/new/xml/%s.xml' % self.inscription_id
    replace_string = u'%s/%s.xml' % ( settings_app.TRANSFORMER_XML_URL_SEGMENT, self.inscription_id )
    self.updated_xslt_html = self.updated_xslt_html.replace( search_string, replace_string )
    return

  def extract_inscription_data(self):
    import bs4
    from bs4 import BeautifulSoup
    ## soupify transformed xml
    soup = BeautifulSoup(
        self.updated_xslt_html,
        [u'lxml', u'xml'],      # says lxml will be the parser, and that the file is xml
        from_encoding=u'utf-8'  # bs4 would figure it out, but this is faster
        ); assert type(soup) == BeautifulSoup, type(soup)
    ## extract summary info
    summary_string = u''
    summary = soup.find( class_=u'titleBlurb' ).find( u'p' )
    if summary:
      for child in summary.children:
          if type(child) == bs4.element.NavigableString:
              summary_string += child.strip()
          elif type(child) == bs4.element.Tag and unicode(child) == u'<br/>':
              summary_string += u'\n'
    ## extract attribute info
    metadata_dict = {}
    attr_metadata = soup.find( class_=u'metadata' )
    if attr_metadata:
      rows = attr_metadata.find_all( u'tr' )
      for row in rows:
          if row.td.attrs[u'class'] == u'label':
              key = row.td.text; assert type(key) == unicode
              value = row.find_all( u'td' )[1].text; assert type(value) == unicode
              metadata_dict[key] = value
    ## extract bib info
    bib_list = []
    bib_metadata = soup.find( class_=u'bibl' )
    bibs = bib_metadata.find_all( u'p' )
    for bib in bibs:
      bib_string = u''
      for i, child in enumerate(bib.children):
        # print u'- child %s is %s, of type %s' % ( i, child, type(child) )
        if type(child) == bs4.element.NavigableString:
          if len( child.strip() )> 0:
            if i == 0:
              bib_string += child.strip()
            else:
              bib_string += u' %s' % child.strip()
        elif type(child) == bs4.element.Tag:
          if child.name == 'i':  # non-unicode; is title
            # print u'- child.name: %s, and type(child.name): %s' % ( child.name, type(child.name) )
            title = child.text.strip()
            # print u'- title is: %s' % title
            if i == 0:
              bib_string += title
            else:
              bib_string += u' %s' % title
      # print u'- bib_string is: %s' % bib_string
      bib_list.append( bib_string.strip() )
    ## assemble data
    self.extracted_data = {
        u'attributes': metadata_dict,
        u'bibl': bib_list,
        u'summary': summary_string
      }
    return

  # end class Inscription2()


# class Inscription(object):

#   def __init__(self):
#     self.inscription_id = None
#     self.inscription_solr_response = None
#     self.inscription_solr_data = None
#     self.image_url = None
#     self.xml_url = None

#   def getInscriptionData(self, inscription_id):
#     """Gets solr inscription data """
#     self.inscription_id = inscription_id
#     sh = SolrHelper()
#     payload = dict( sh.default_params.items() + {
#       u'q': u'id:%s' % inscription_id,
#       u'rows': u'99999' }.items()
#       )
#     r = requests.get( settings_app.SOLR_URL, params=payload )
#     log.debug( u'inscription solr call: %s' % r.url )
#     self.inscription_solr_response = r.content.decode( u'utf-8', u'replace' )
#     jdict = json.loads( self.inscription_solr_response )
#     self.inscription_solr_data = jdict[u'response'][u'docs'][0]; assert type(self.inscription_solr_data) == dict
#     log.debug( u'self.inscription_solr_data: %s' % self.inscription_solr_data )
#     return

#   def updateData(self):
#     ## handle non-keys
#     for entry in [
#       u'bib_authors',
#       u'condition',
#       u'decoration',
#       u'material',
#       u'msid_repository',
#       u'msid_settlement',
#       u'object_type',
#       u'text_genre',
#       u'writing' ]:
#       if entry not in self.inscription_solr_data.keys():
#         self.inscription_solr_data[ entry ] = None
#     ## image url
#     images_listing = os.listdir( u'%s/usep/images/inscriptions/' % settings_project.STATIC_ROOT )
#     if u'%s.jpg' % self.inscription_id in images_listing:
#       self.image_url = u'%s/usep/images/inscriptions/%s.jpg' % ( settings_project.STATIC_URL, self.inscription_id )
#     else:
#       self.image_url = None
#     ## xml url
#     self.xml_url = u'%s/%s.xml' % ( settings_app.XML_URL_SEGMENT, self.inscription_id )
#     return

#   # end class Inscription()


class Publication(object):

  def __init__(self):
    self.title = u''
    self.inscription_count = 0
    self.inscription_entries = []
    self.inscription_images = []  # used for thumbnails
    self.pub_solr_urls = []
    self.pub_solr_responses = []
    self.facets = None
    self.kochief = Kochief()
    try:
      self.page_object = Page.objects.using(settings_app.DB).get(head_title="Publication")
    except ObjectDoesNotExist:
      self.page_object = Page(head_title="Publication")
      self.page_object.save(using=settings_app.DB)

  def getPubData( self, id_list ):
    """
    Builds solr query from inscription-id list stored in session by Publications.buildPubLists().
    We have the ids already; we just need the status (possible TODO: store the status when the id-list is originally built).
    Loop used because a large list can return a solr 'too many boolean clauses' error
    
    There's a problem with pagination this way: Because we are limiting it to the IDs that are in any single page, the facet
    counts that are returned are returned on that sublist of queries. We should let solr take care of pagination instead of
    caching a pubs.getpubdata response. 
    """

    log.debug( u'len(id_list): %s' % len(id_list) )
    log.debug( u'id_list: %s' % id_list )
    # log.debug( u'self.inscription_entries START: %s' % self.inscription_entries )
    # log.debug( u'len(self.inscription_entries) START: %s' % len(self.inscription_entries) )
    id_list = sorted(id_list)
    try:
      page = int(self.kochief.page_str)
    except TypeError, ValueError:
      page = 1
    assert(page > 0)
    q_start = (page - 1) * settings_app.ITEMS_PER_PAGE
    q_rows = min( int(settings_app.ITEMS_PER_PAGE), 500 )
    q_max = min( len(id_list), q_start + q_rows )
    if q_start > len(id_list):
      raise IndexError('Page number exceeds total number of pages.')
      return
    for i in range( q_start, q_max, q_rows ):  # needed
      q_string = u'id:"%s"' % id_list[i]
      list_chunk = id_list[i+1:i+q_rows]
      ## make solr call
      for entry in list_chunk:
          q_string = u'%s OR id:"%s"' % ( q_string, entry )
      payload = {
        u'rows': u'99999',
        u'fl': u'id, status',
        u'sort': u'id asc'
      }
      payload.update(self.page_object.facet_params(payload['fl']))
      self.kochief.get_params_from_query(q_string)
      r, jdict = self.kochief.get_solr_response(params = payload)
      solr_response = r.content.decode(u'utf-8', u'replace')
      log.debug( u'this pubn_solr_url: %s' % r.url )
     # log.debug( u'this pubn_solr_response: %s' % solr_response )
      self.pub_solr_urls.append( r.url )
      self.pub_solr_responses.append( solr_response )
      for item in jdict[u'response'][u'docs']:
        self.inscription_entries.append( item )
    self.inscription_count = len( id_list )
    self.solr_start = q_start + 1
    self.solr_count = jdict[u'response'][u'numFound']
    self.facets = Facet.render(jdict[u'facet_counts'][u'facet_fields'])

    #log.debug( u'self.inscription_entries END: %s' % self.inscription_entries[0:10] )
    return

  def buildInscriptionList( self, url_scheme, server_name ):
    """Adds item-url to inscription-dict list."""
    for item in self.inscription_entries:
      item[u'url'] = u'%s://%s%s' % ( url_scheme, server_name, reverse(u'inscription_url', args=(item[u'id'],)) )
    return

  def makeImageUrls( self ):
    """Adds image_url to inscription-dict list."""
    ## get list of inscription images
    inscription_images_dir = u'%s/usep/images/inscriptions/' % settings_project.STATIC_ROOT
    self.inscription_images = os.listdir( inscription_images_dir )
    ## check items against them
    for item in self.inscription_entries:
      if u'%s.jpg' % item[u'id'] in self.inscription_images:
        item[u'image_url'] = u'%s/usep/images/inscriptions/%s.jpg' % ( settings_project.STATIC_URL, item[u'id'] )
      else:
        item[u'image_url'] = None
    return

  # end class Publication()


class Publications(object):

  def __init__(self):
    self.corpora = []  # list for display
    self.corpora_dict = {}  # dict of key=title & value=inscription_id list
    self.journals = []
    self.journals_dict = {}
    self.monographs = []
    self.monographs_dict = {}
    self.master_pub_dict = {}
    self.pubs_solr_url = None
    self.pubs_solr_response = None
    self.pubs_entries = None
    self.kochief = Kochief()
    self.facets = []
    try:
      self.page_object = Page.objects.using(settings_app.DB).get(head_title="Publications")
    except ObjectDoesNotExist:
      self.page_object = Page(head_title="Publications")
      self.page_object.save(using=settings_app.DB)

  def getPubData(self):
    """Gets solr publication data for self.buildPubLists()"""
    payload = {
      u'rows': u'99999',
      u'fl': u'id, bib_ids, bib_ids_types, bib_titles, bib_titles_all, status'
    }
    payload.update(self.page_object.facet_params(payload['fl']))
    self.kochief.get_params_from_query(u'bib_ids_types:*')
    r, jdict = self.kochief.get_solr_response(payload)

    log.debug(r.text)
    log.debug( u'publications solr call: %s' % r.url )
    self.pubs_solr_url = r.url
    self.pubs_solr_response = r.content.decode( u'utf-8', u'replace' )
    log.debug( u'publications solr query result dict keys.response: %s' % jdict.keys() )
    log.debug( u'publications solr query result dict["response"] keys: %s' % jdict[u'response'].keys() )
    log.debug( u'publications solr query result dict["response"]["numFound"]: %s' % jdict[u'response'][u'numFound'] )
    log.debug( u'publications solr query result dict["response"]["docs"][0]: %s' % jdict[u'response'][u'docs'][0:5] )
    self.pubs_entries = jdict[u'response'][u'docs']
    self.facets = Facet.render(jdict[u'facet_counts'][u'facet_fields'])
    
    # log.debug( u'self.pubs_entries: %s' % self.pubs_entries )

  def buildPubLists(self):
    """Builds list of publications grouped by type."""
    # log.debug( u'self.pubs_entries: %s' % self.pubs_entries )
    log.debug( u'len( self.pubs_entries ): %s' % len( self.pubs_entries ) )
    corpora_dict = {}; journal_dict = {}; monograph_dict = {}  # temp holders
    for entry in self.pubs_entries:  # an entry can contain multiple bibs
      # log.debug( u'entry being processed: %s' % entry )
      ## make separate bib entries
      temp_bibs = []
      last_bib_type = None
      for i, bib_id in enumerate( entry[u'bib_ids'] ):
        try:
          last_bib_type = entry[u'bib_ids_types'][i]  # first should always succeed
        except:
          pass
        try:
          bib_title = entry[u'bib_titles_all'][i]
        except:
          bib_title = u'title not found for bib_id "%s"' % bib_id
        try:
          bib_status = entry[u'status']
        except:
          bib_status = u'no_status'
        temp_bibs.append( {
          u'bib_id': bib_id,
          u'bib_title': bib_title,
          u'bib_type': last_bib_type,
          u'id': entry[u'id'],  # the inscription_id
          u'status': bib_status
          } )
      # log.debug( u'temp_bibs: %s' % temp_bibs )
      ## categorize by bib_type
      for bib in temp_bibs:
        ## update master dict
        # self.master_pub_dict[ bib[u'bib_title'] ] = { u'id': bib[u'id'], u'status': bib[u'status'] }
        if bib[u'bib_title'] in self.master_pub_dict.keys():
          self.master_pub_dict[ bib[u'bib_title'] ].append( bib[u'id'] )
        else:
          self.master_pub_dict[ bib[u'bib_title'] ] = [ bib[u'id'] ]
        ## update type-dicts
        if bib['bib_type'] == u'corpora':
          if bib[u'bib_title'] in corpora_dict.keys():
            corpora_dict[ bib[u'bib_title'] ].append( bib[u'id'] )
          else:
            corpora_dict[ bib[u'bib_title'] ] = [ bib[u'id'] ]
        elif bib['bib_type'] == u'journal':
          if bib[u'bib_title'] in journal_dict.keys():
            journal_dict[ bib[u'bib_title'] ].append( bib[u'id'] )
          else:
            journal_dict[ bib[u'bib_title'] ] = [ bib[u'id'] ]
        elif bib['bib_type'] == u'monograph':
          # log.debug( u'bib_type is monograph' )
          if bib[u'bib_title'] in monograph_dict.keys():
            monograph_dict[ bib[u'bib_title'] ].append( bib[u'id'] )
          else:
            monograph_dict[ bib[u'bib_title'] ] = [ bib[u'id'] ]
        # log.debug( u'monograph_dict is now: %s' % monograph_dict )
    ## store
    self.corpora_dict = corpora_dict
    self.corpora = sorted( self.corpora_dict.keys() )
    self.journals_dict = journal_dict
    self.journals = sorted( self.journals_dict.keys() )
    self.monographs_dict = monograph_dict
    self.monographs = sorted( self.monographs_dict.keys() )
    # log.debug( u'corpora list before sort: %s' % self.corpora )
    return

  # end class Publications()
