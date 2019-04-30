from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from home import views
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

class views_test(TestCase):
    def test_view1(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('aboutus'))
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name1(self):
        response = self.client.get(reverse('contact'))
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name3(self):
        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name4(self):
        response = self.client.get(reverse('stats'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('aboutus'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/aboutus.htm')

    def test_view_uses_correct_template1(self):
        response = self.client.get(reverse('contact'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact.htm')

    def test_view_uses_correct_template2(self):
        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/profile.htm')

    def test_view_uses_correct_template3(self):
        response = self.client.get(reverse('stats'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/stats.htm')
