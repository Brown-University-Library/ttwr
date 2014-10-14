from django.db import models

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
# BDRItem
# Book
# Page
# Print
