# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from . import views
from . import models


def get_auth_client():
    username = 'someone@brown.edu'
    password = 'pw'
    u = User.objects.create_user(username, password=password)
    auth_client = Client()
    logged_in = auth_client.login(username=username, password=password)
    if not logged_in:
        raise Exception('couldn\'t log in user')
    return auth_client


class TestStaticViews(TestCase):

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The Theater that was Rome')

    def test_about(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>About</h2>')

    def test_links(self):
        response = self.client.get(reverse('links'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<li>Links</li>')

    def test_search(self):
        #this page is static as far as the django view is concerned
        response = self.client.get(reverse('search_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rome - Search')


class TestPageDetail(TestCase):

    def test_1(self):
        response = self.client.get(reverse('book_page_viewer', kwargs={'book_id': '230605', 'page_id': '230606'}))
        self.assertEqual(response.status_code, 200)

    def test_get_next_prev_pids(self):
        prev_id, next_id = views._get_prev_next_ids({'relations': {'hasPart': []}}, None)
        self.assertEqual(prev_id, 'none')
        self.assertEqual(next_id, 'none')
        hasPart_data = [
                {'pid': 'test:111', 'order': '1'},
                {'pid': 'test:112', 'order': '2'},
                {'pid': 'test:113', 'order': '3'},
                ]
        prev_id, next_id = views._get_prev_next_ids({'relations': {'hasPart': hasPart_data}}, 'test:112')
        self.assertEqual(prev_id, '111')
        self.assertEqual(next_id, '113')
        hasPart_data = [
                {'pid': 'test:111', 'order': '1'},
                {'pid': 'test:112', 'order': '1-3'},
                {'pid': 'test:113', 'order': '3'},
                ]
        prev_id, next_id = views._get_prev_next_ids({'relations': {'hasPart': hasPart_data}}, 'test:112')
        self.assertEqual(prev_id, '111')
        self.assertEqual(next_id, '113')


class TestRecordCreatorViews(TestCase):

    def test_new_genre_auth(self):
        response = self.client.get(reverse('new_genre'))
        self.assertRedirects(response, 'http://testserver/rome/login/?next=/rome/genres/new/')

    def test_new_genre(self):
        auth_client = get_auth_client()
        response = auth_client.get(reverse('new_genre'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Text')

    def test_new_genre_post(self):
        auth_client = get_auth_client()
        self.assertEqual(len(models.Genre.objects.all()), 0)
        response = auth_client.post(reverse('new_genre'), {'text': 'Book'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'opener.dismissAddAnotherPopup(window, "1", "Book");')
        self.assertEqual(len(models.Genre.objects.all()), 1)
        self.assertEqual(models.Genre.objects.all()[0].text, 'Book')

    def test_new_role_auth(self):
        response = self.client.get(reverse('new_role'))
        self.assertRedirects(response, 'http://testserver/rome/login/?next=/rome/roles/new/')

    def test_new_role(self):
        auth_client = get_auth_client()
        response = auth_client.get(reverse('new_role'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Text')

    def test_new_role_post(self):
        auth_client = get_auth_client()
        self.assertEqual(len(models.Role.objects.all()), 0)
        response = auth_client.post(reverse('new_role'), {'text': u'Auth©r'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'opener.dismissAddAnotherPopup(window, "1", "Auth©r");')
        self.assertEqual(len(models.Role.objects.all()), 1)
        self.assertEqual(models.Role.objects.all()[0].text, u'Auth©r')

    def test_new_biography_auth(self):
        response = self.client.get(reverse('new_biography'))
        self.assertRedirects(response, 'http://testserver/rome/login/?next=/rome/biographies/new/')

    def test_new_biography(self):
        auth_client = get_auth_client()
        response = auth_client.get(reverse('new_biography'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Name')

    def test_new_biography_post(self):
        models.Biography.objects.create(name='Tom', trp_id='0001')
        auth_client = get_auth_client()
        self.assertEqual(len(models.Biography.objects.all()), 1)
        response = auth_client.post(reverse('new_biography'), {'name': u'Säm', 'trp_id': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'opener.dismissAddAnotherPopup(window, "2", "Säm (0002)");')
        self.assertEqual(len(models.Biography.objects.all()), 2)
        self.assertEqual(models.Biography.objects.all()[0].name, u'Säm')
