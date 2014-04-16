from django.db import models


class Biography(models.Model):

    name = models.CharField(max_length=254)
    trp_id = models.CharField(max_length=15, unique=True)
    external_id = models.CharField(max_length=254, unique=True, null=True, blank=True)
    bio = models.TextField()


class Essay(models.Model):

    slug = models.SlugField(max_length=254)
    author = models.CharField(max_length=254)
    title = models.CharField(max_length=254)
    text = models.TextField()

