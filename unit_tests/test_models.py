# -*- coding: utf-8 -*-
from django.test import TestCase
from rome_app import models


class TestBiography(TestCase):

    def test_trp(self):
        b = models.Biography.objects.create()
        self.assertEqual(b.trp_id, '0001')
        b = models.Biography.objects.create(trp_id=5)
        self.assertEqual(b.trp_id, '0005')

    def test_roles(self):
        b = models.Biography.objects.create(roles='author,painter')
        self.assertEqual(b.roles, 'author;painter')
