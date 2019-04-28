from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from accounts.views import SignUp

#from accounts.models import
#
# class TestViews(TestCase):
#     def test_something(self):
#         client = Client()
#         response = client.get(reverse('list'))
#
#         self.assertEquals(response.status_code, 200 )
class views_test(TestCase):
    def test_view0(self):
        data = {'username': 'testclient',
                    'password1': 'test123',
                    'password2': 'test123',}
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())

    def test_view1(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_sign_up_contains_correct_html0(self):
        response = self.client.get('/')
        self.assertNotContains(response, '<h2><font color="white">Sign up</font></h2> ')

    def test_sign_up_contains_correct_html1(self):
        response = self.client.get('/')
        self.assertNotContains(response, 'Sign up')

    def test_sign_up_does_not_contain_incorrect_html0(self):
        response = self.client.get('/')
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')

    def test_sign_up_does_not_contain_incorrect_html1(self):
        response = self.client.get('/')
        self.assertNotContains(
            response, 'Sign up')

    def test_sign_up_does_not_contain_correct_html1(self):
        response = self.client.get('/')
        self.assertContains(
            response, 'login')

    def setUp(self):
        self.client = Client()

    def setup1(self):
        user = auth.get_user(response.wsgi_request)
        assert user.is_authenticated()

    def testLogin(self):
        response = self.client.post('/signup', {'username': 'Donk',
                    'password1': 'InTimidator23',
                    'password2': 'InTimidator23'})
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_details(self):
        request = self.factory.get('accounts/signup')
        request.user = self.user
        response = SignUp.as_view()(request)
        self.assertEqual(response.status_code, 200)
