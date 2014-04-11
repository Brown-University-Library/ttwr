from django.db import models


class Biography(models.Model):

    name = models.CharField(max_length=254)
    trp_id = models.CharField(max_length=15)
    bio = models.TextField()


class Essay(models.Model):

    author = models.CharField(max_length=254)
    title = models.CharField(max_length=254)

