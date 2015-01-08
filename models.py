from django.http import Http404
from django.db import models
from django.core.urlresolvers import reverse
from .  import app_settings
import requests
import json
from bdrxml import mods

# Database Models
class Biography(models.Model):

    name = models.CharField(max_length=254, help_text='Enter name as it appears in the book metadata')
    trp_id = models.CharField(max_length=15, unique=True, help_text='Enter TRP id as a 4-digit number, eg. 0023')
    alternate_names = models.CharField(max_length=254, null=True, blank=True, help_text='Optional: enter alternate names separated by a semi-colon')
    external_id = models.CharField(max_length=254, null=True, blank=True, help_text='Optional: enter Ulan id in the form of a URL; if there is no Ulan id, enter LCCN in the form of a URL')
    birth_date = models.CharField(max_length=25, null=True, blank=True, help_text='Optional: enter birth date as yyyy-mm-dd (for sorting and filtering)')
    death_date = models.CharField(max_length=25, null=True, blank=True, help_text='Optional: enter death date as yyyy-mm-dd')
    roles = models.CharField(max_length=254, null=True, blank=True, help_text='Optional: enter roles, separated by a semi-colon')
    bio = models.TextField()

    class Meta:
        verbose_name_plural = 'biographies'
        ordering = ['name']


    def books(self):
        return Book.search(query='name:"%s"' % self.name )

    def prints(self):
        return Print.search(query='contributor:"%s"' % self.name )

class Essay(models.Model):

    slug = models.SlugField(max_length=254)
    author = models.CharField(max_length=254)
    title = models.CharField(max_length=254)
    text = models.TextField()

# Non-Database Models
class BDRObject(object):
    def __init__(self, data=None, parent=None):
        self.data= data or {}
        self.parent= parent

    def __nonzero__(self):
        return bool(self.data)

    def __getattr__(self, name):
        if name in self.data:
            return self.data.get(name)
        else:
            raise AttributeError

    OBJECT_TYPE = "*"
    @classmethod
    def search(cls, query="*", rows=6000):
        url1 = 'https://%s/api/pub/collections/621/?q=%s&fq=object_type:%s&fl=*&fq=discover:BDR_PUBLIC&rows=%s' % (app_settings.BDR_SERVER, query, cls.OBJECT_TYPE, rows)
        objects_json = json.loads(requests.get(url1).text)
        num_objects = objects_json['items']['numFound']
        if num_objects>rows: #only reload if we need to find more bdr_objects
            return cls.search(query, num_objects)
        return [ cls(data=obj_data) for obj_data in objects_json['items']['docs'] ]


    @classmethod
    def get(cls, pid):
        json_uri='https://%s/api/pub/items/%s/?q=*&fl=*' % (app_settings.BDR_SERVER, pid)
        resp = requests.get(json_uri)
        if not resp.ok:
             return cls()
        return cls(data=json.loads(resp.text))

    @classmethod
    def get_or_404(cls, pid):
        obj = cls.get(pid)
        if not obj:
            raise Http404
        return obj


    @property
    def id(self):
        return self.data.get('pid','').split(":")[-1]

    def _get_full_title(self):
        data = self.data
        if 'nonsort' not in data:
            return u'%s' % data['primary_title']
        if data['nonsort'].endswith(u"'"):
            return u'%s%s' % (data['nonsort'], data['primary_title'])
        return u'%s %s' % (data['nonsort'], data['primary_title'])

    @property
    def studio_uri(self):
        return self.uri

    def title(self):
        return self._get_full_title()

    def alt_titles(self):
        if "mods_title_alt" in self.data:
            return self.mods_title_alt
        return []

    def date(self):
        if "dateCreated" in self.data:
            return self.dateCreated[0:4]
        if "dateIssued" in self.data:
            return self.dateIssued[0:4]
        return "n.d"

    def authors(self):
        if "contributor_display" in self.data:
            return "; ".join(self.contributor_display)
        return "contributor(s) not available"

    @property
    def thumbnail_src(self):
        return 'https://%s/viewers/image/thumbnail/%s/' % (app_settings.BDR_SERVER, self.pid)

from django.utils.datastructures import SortedDict
# Book
class Book(BDRObject):
    OBJECT_TYPE = "implicit-set"
    CUTOFF = 80
    SORT_OPTIONS = SortedDict([
        ( 'authors', 'authors' ),
        ( 'title', 'title' ),
        ( 'date', 'date' ),
    ])

    @property
    def thumbnail_url(self):
        return  reverse('thumbnail_viewer', kwargs={'book_id': self.id})

    @property
    def short_title(self):
        if self.title_cut():
            return self.title()[0:Book.CUTOFF-3]+"..."
        return self.title()

    def title_cut(self):
        return bool(len(self.title()) > Book.CUTOFF)

    def port_url(self):
        return 'https://%s/viewers/readers/portfolio/%s/' % (app_settings.BDR_SERVER, self.pid)

    def book_url(self):
        return 'https://%s/viewers/readers/set/%s/' % (app_settings.BDR_SERVER, self.pid)

    def pages(self):
        return [ Page(data=page_data, parent=self) for page_data in self.relations['hasPart'] ]


# Page
class Page(BDRObject):
    OBJECT_TYPE = "implicit-set" #TODO change to something more page appropriate

    def embedded_viewer_src(self):
        return 'https://%s/viewers/image/zoom/%s/' % (app_settings.BDR_SERVER, self.pid)

    def url(self):
        return reverse('book_page_viewer', args=[self.parent.id, self.id])

# Print
class Print(Page):
    OBJECT_TYPE = "image-compound"

    def url(self):
        return reverse('specific_print', args=[self.id,])


class Annotation(object):

    @classmethod
    def from_form_data(cls, page_pid, form_data, person_formset_data):
        return cls(page_pid, form_data=form_data, person_formset_data=person_formset_data)

    def __init__(self, page_pid, form_data=None, person_formset_data=None, mods_obj=None):
        self._page_pid = page_pid
        self._form_data = form_data
        self._person_formset_data = [p for p in person_formset_data if p]
        self._mods_obj = mods_obj

    def get_mods_obj(self):
        if not self._mods_obj:
            self._mods_obj = mods.make_mods()
            self._mods_obj.title = self._form_data['title_orig']
            if self._person_formset_data:
                for p in self._person_formset_data:
                    name = mods.Name()
                    np = mods.NamePart(text=p['name'])
                    name.name_parts.append(np)
                    role = mods.Role(text=p['role'])
                    name.roles.append(role)
                    href = '{%s}href' % app_settings.XLINK_NAMESPACE
                    name.node.set(href, p['trp_id'])
                    self._mods_obj.names.append(name)
        return self._mods_obj

    def to_mods_xml(self):
        return self.get_mods_obj().serialize()

    def _get_params(self):
        params = {'identity': app_settings.BDR_IDENTITY, 'authorization_code': app_settings.BDR_AUTH_CODE}
        params['mods'] = json.dumps({u'xml_data': self.to_mods_xml()})
        params['rels'] = json.dumps({u'isAnnotationOf': self._page_pid})
        params['rights'] = json.dumps({'parameters': {'owner_id': app_settings.BDR_ADMIN, 'additional_rights': '%s#modify+BDR_PUBLIC#discover,display' % app_settings.BDR_IDENTITY}})
        params['content_model'] = 'Annotation'
        return params

    def save_to_bdr(self):
        params = self._get_params()
        r = requests.post(app_settings.BDR_POST_URL, data=params)
        if r.ok:
            return {'pid': json.loads(r.text)['pid']}
        else:
            raise Exception('error posting new annotation for %s: %s - %s' % (self._page_pid, r.status_code, r.content))

