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


class TestBooksViews(TestCase):

    def test_new_annotation_auth(self):
        url = reverse('new_annotation', kwargs={'book_id': '230605', 'page_id': '230606'})
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (reverse('rome_login'), url))

    def test_new_annotation_get(self):
        auth_client = get_auth_client()
        url = reverse('new_annotation', kwargs={'book_id': '230605', 'page_id': '230606'})
        response = auth_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="Submit Annotation"')

    def test_edit_annotation_auth(self):
        url = reverse('edit_annotation', kwargs={'book_id': '224807', 'page_id': '224895', 'anno_id': '228874'})
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (reverse('rome_login'), url))

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


class TestPrintsViews(TestCase):

    def test_new_print_annotation_auth(self):
        url = reverse('new_print_annotation', kwargs={'print_id': '230631'})
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (reverse('rome_login'), url))

    def test_new_print_annotation_get(self):
        auth_client = get_auth_client()
        url = reverse('new_print_annotation', kwargs={'print_id': '230631'})
        response = auth_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="Submit Annotation"')

    def test_edit_print_annotation_auth(self):
        url = reverse('edit_print_annotation', kwargs={'print_id': '230631', 'anno_id': '230632'})
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (reverse('rome_login'), url))


class TestEssaysViews(TestCase):

    def test_essays(self):
        response = self.client.get(reverse('essays'))
        self.assertEqual(response.status_code, 200)
        models.Essay.objects.create(slug='ger', author='David Ortiz', title=u'Rëd Sox')
        response = self.client.get(reverse('essays'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'Rëd Sox')

    def test_specific_essay(self):
        models.Essay.objects.create(slug='ger', author='David Ortiz', title=u'Rëd Sox', text='### Red Sox lineup[^n1]\n\n[^n1]: footnote text')
        response = self.client.get(reverse('specific_essay', kwargs={'essay_slug': 'ger'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h3>Red Sox lineup') #make sure that basic markdown was rendered
        self.assertContains(response, '<p>footnote text') #make sure that footnote was rendered


class TestPeopleViews(TransactionTestCase):

    def test_people(self):
        models.Biography.objects.create(name=u'Frëd', trp_id='0001')
        response = self.client.get(reverse('people'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u'Frëd')


class TestRecordCreatorViews(TestCase):

    def test_new_genre_auth(self):
        url = reverse('new_genre')
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (reverse('rome_login'), url))

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
        url = reverse('new_role')
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (reverse('rome_login'), url))

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
        url = reverse('new_biography')
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (reverse('rome_login'), url))

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

class TestUtilityFunctions(TestCase):
    
    def test_firstword_content(self):
        self.assertEqual(views.first_word("title sentence here"), "title")
        self.assertEqual(views.first_word("title"), "title")

    def test_firstword_nulls(self):
        self.assertEqual("", views.first_word(""))
        self.assertEqual("", views.first_word(None))

