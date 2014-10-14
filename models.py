from django.db import models
from django.core.urlresolvers import reverse
from .app_settings import BDR_SERVER

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

class Essay(models.Model):

    slug = models.SlugField(max_length=254)
    author = models.CharField(max_length=254)
    title = models.CharField(max_length=254)
    text = models.TextField()

# Non-Database Models
class BDRObject(object):
    def __init__(self, data=None):
        self.data= data or {}

    def __nonzero__(self):
        return bool(self.data)

    def __getattr__(self, name):
        if name in self.data:
            return self.data.get(name)
        else:
            raise AttributeError
# Book
class Book(BDRObject):
    CUTOFF = 80

    @property
    def pid(self):
        return self.data.get('pid','').split(":")[-1]

    @property
    def thumbnail_url(self):
        return  reverse('thumbnail_viewer', kwargs={'book_pid': self.pid})

    @property
    def studio_uri(self):
        return self.uri

    def title(self):
        return self._get_full_title()

    @property
    def short_title(self):
        if self.title_cut():
            return self.title()[0:Book.CUTOFF-3]+"..."
        return self.title()

    def title_cut(self):
        return bool(len(self.title()) > Book.CUTOFF)

    def _get_full_title(self):
        data = self.data
        if 'nonsort' not in data:
            return u'%s' % data['primary_title']
        if data['nonsort'].endswith(u"'"):
            return u'%s%s' % (data['nonsort'], data['primary_title'])
        return u'%s %s' % (data['nonsort'], data['primary_title'])

    def port_url(self):
        return 'https://%s/viewers/readers/portfolio/bdr:%s/' % (BDR_SERVER, self.pid)

    def book_url(self):
        return 'https://%s/viewers/readers/set/bdr:%s/' % (BDR_SERVER, self.pid)

    def authors(self):
        if "contributor_display" in self.data:
            return "; ".join(self.contributor_display)
        return "contributor(s) not available"

    def date(self):
        if "dateCreated" in self.data:
            return self.dateCreated[0:4]
        if "dateIssued" in self.data:
            return self.dateIssued[0:4]
        return "n.d"


# Page
# Print
