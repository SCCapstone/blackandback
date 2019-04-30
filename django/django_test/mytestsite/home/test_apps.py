from django.apps import AppConfig
from django.test import TestCase
from home.apps import HomeConfig

class apps_test(TestCase):
    def test_apps0(self):
        self.assertEqual(HomeConfig.name, 'home')
