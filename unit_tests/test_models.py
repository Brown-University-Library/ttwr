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

class TestEssay(TestCase):

    def test_preview(self):
        e = models.Essay.objects.create(slug='test', author='Test Author', title='Test Title')
        self.assertEqual(e.preview(), '')

    def test_get_related_works_query(self):
       #test essay with pids
       e = models.Essay.objects.create(slug='test', author='Test Author', title='Test Title', pids="123,456")
       query = "ir_collection_id:621+AND+display:BDR_PUBLIC+AND+(pid:'bdr:123'+OR+pid:'bdr:456')&fl=primary_title,rel_has_pagination_ssim,rel_is_part_of_ssim,creator,pid,genre"
       self.assertEqual(e._get_related_works_query(), query)
       #test essay with no pids
       e = models.Essay.objects.create(slug='test', author='Test Author', title='Test Title')
       self.assertEqual(e._get_related_works_query(), ??)