from django.test import TestCase
from django.urls import reverse, resolve
from accounts.views import SignUp

class TestUrls(TestCase):
    def test_signup_path_is_resolved(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, SignUp)
