from django.db import models


class Biography(models.Model):

    name = models.CharField(max_length=254, help_text='Enter name as it appears in the book metadata')
    alternate_names = models.CharField(max_length=254, null=True, blank=True, help_text='Optional: enter alternate names')
    trp_id = models.CharField(max_length=15, unique=True, help_text='Enter TRP id as a 4-digit number, eg. 0023')
    external_id = models.CharField(max_length=254, unique=True, null=True, blank=True, help_text='Optional: enter Ulan id in the form of a URL; if there is no Ulan id, enter LCCN in the form of a URL')
    birth_date = models.CharField(max_length=25, null=True, blank=True, help_text='Optional: enter date of birth in w3cdtf format')
    death_date = models.CharField(max_length=25, null=True, blank=True, help_text='Optional: enter date of death in w3cdtf format')
    roles = models.CharField(max_length=254, null=True, blank=True, help_text='Optional: enter roles, separated by spaces')
    bio = models.TextField()

    class Meta:
        verbose_name_plural = 'biographies'

class Essay(models.Model):

    slug = models.SlugField(max_length=254)
    author = models.CharField(max_length=254)
    title = models.CharField(max_length=254)
    text = models.TextField()

