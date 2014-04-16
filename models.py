from django.db import models


class Biography(models.Model):

    name = models.CharField(max_length=254, help_text='Enter name as it appears in the book metadata')
    trp_id = models.CharField(max_length=15, unique=True, help_text='Enter TRP id as a 4-digit number, eg. 0023')
    external_id = models.CharField(max_length=254, unique=True, null=True, blank=True, help_text='Enter Ulan id in the form of a URL; if there is no Ulan id, enter LCCN in the form of a URL')
    bio = models.TextField()

    class Meta:
        verbose_name_plural = 'biographies'

class Essay(models.Model):

    slug = models.SlugField(max_length=254)
    author = models.CharField(max_length=254)
    title = models.CharField(max_length=254)
    text = models.TextField()

