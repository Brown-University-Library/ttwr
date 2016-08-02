from django.core.urlresolvers import reverse
from django.test import TestCase


class TestPageDetail(TestCase):

    def test_1(self):
        response = self.client.get(reverse('book_page_viewer', kwargs={'book_id': '230605', 'page_id': '230606'}))
        self.assertEqual(response.status_code, 200)
