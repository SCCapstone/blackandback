from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import SignUp

class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func.view_class, SignUp)