from django.db import models
from django import forms
from django.utils.encoding import smart_unicode

# Create your models here.

# class AboutPage(models.Model):
# 	title_for_tab = models.CharField(blank=True, max_length=100)
# 	title_for_content = models.CharField(blank=True, max_length=100)
# 	page_content = models.TextField(blank=True, help_text='write page content here')
# 	def __unicode__(self):
# 		return smart_unicode(self.title_for_tab, u'utf-8', u'replace')
# 	class Meta:
# 		verbose_name = u'About page fields'
		
class About(models.Model):
    header = models.CharField( blank=True, max_length=50, help_text=u'header')
    description = models.TextField( blank=True, max_length=10000, help_text=u'description' )

	def __unicode__(self):
    	return smart_unicode( self.description, u'utf-8', u'replace' )
    class Meta:
    	verbose_name = u'About page fields'

# end class About()