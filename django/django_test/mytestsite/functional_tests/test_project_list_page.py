from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

class TestProjectListPage(StaticLiveServerTestCase):
    def test_foo(self):
        self.assertEquals(0,1)
