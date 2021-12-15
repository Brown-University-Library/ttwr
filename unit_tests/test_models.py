from django.conf import settings
from django.db import IntegrityError
from django.test import SimpleTestCase, TestCase
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
       query = f'rel_is_member_of_collection_ssim:"{settings.TTWR_COLLECTION_PID}"+AND+display:BDR_PUBLIC+AND+(pid:"testsuite:123"+OR+pid:"testsuite:456")&fl=primary_title,rel_has_pagination_ssim,rel_is_part_of_ssim,creator,pid,genre'
       self.assertEqual(models.get_related_works_query(e.pids), query)
       #test essay with no pids
       e = models.Essay.objects.create(slug='test', author='Test Author', title='Test Title')
       self.assertEqual(models.get_related_works_query(e.pids), None)


class TestDocument(TestCase):

    def test_unique(self):
        d = models.Document.objects.create(slug='1', consagra=True)
        with self.assertRaises(IntegrityError):
            models.Document.objects.create(slug='1', consagra=True)


class TestBDRObject(SimpleTestCase):

    def test_init(self):
        b = models.BDRObject()
        self.assertFalse(b)

