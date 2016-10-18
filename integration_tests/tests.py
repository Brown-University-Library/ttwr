# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, TransactionTestCase, Client
from rome_app import views
from rome_app import models


def get_auth_client():
    username = 'someone@brown.edu'
    password = 'pw'
    u = User.objects.create_user(username, password=password)
    auth_client = Client()
    logged_in = auth_client.login(username=username, password=password)
    if not logged_in:
        raise Exception('couldn\'t log in user')
    return auth_client


class TestBooksViews(TestCase):

    def test_books(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rome - Books')

    def test_book_thumbnail_viewer(self):
        response = self.client.get(reverse('thumbnail_viewer', kwargs={'book_id': '230605'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book 230605')

    def test_book_page_viewer(self):
        response = self.client.get(reverse('book_page_viewer', kwargs={'book_id': '230605', 'page_id': '230606'}))
        self.assertEqual(response.status_code, 200)

    def test_edit_annotation_get(self):
        bio = models.Biography.objects.create(trp_id='2225')
        role = models.Role.objects.create(text='Engraver')
        auth_client = get_auth_client()
        url = reverse('edit_annotation', kwargs={'book_id': '224807', 'page_id': '224895', 'anno_id': '228874'})
        response = auth_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="Submit Annotation"')


class TestPrintsViews(TestCase):

    def test_prints(self):
        response = self.client.get(reverse('prints'))
        self.assertEqual(response.status_code, 200)

    def test_specific_print(self):
        response = self.client.get(reverse('specific_print', kwargs={'print_id': 230631}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ARTES ATHENIX PARTHENOPEM')

    def test_edit_print_annotation_get(self):
        auth_client = get_auth_client()
        url = reverse('edit_print_annotation', kwargs={'print_id': '230631', 'anno_id': '230632'})
        response = auth_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="Submit Annotation"')


class TestPeopleViews(TransactionTestCase):

    def test_person_detail(self):
        models.Biography.objects.create(name=u'Frëd', trp_id='0001', bio=u'### Frëd')
        response = self.client.get(reverse('person_detail', kwargs={'trp_id': '0001'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'<h3>Frëd</h3>')
