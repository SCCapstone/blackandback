from django.conf.urls import url
from django.test import TestCase, Client
from django.urls import reverse, resolve
import home.urls

class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()

    def test_url0(self):
        url = reverse('aboutus')
        self.assertEquals(url, '/aboutus')

    def test_url1(self):
        url = reverse('contact')
        self.assertEquals(url, '/contact')

    def test_url2(self):
        url = reverse('featured_photos')
        self.assertEquals(url, '/featured_photos')

    def test_url3(self):
        url = reverse('profile')
        self.assertEquals(url, '/profile')

    def test_url4(self):
        url = reverse('stats')
        self.assertEquals(url, '/stats')
