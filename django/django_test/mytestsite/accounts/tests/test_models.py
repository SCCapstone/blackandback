from django.test import TestCase
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from accounts.forms import SignUpForm
import inspect
from django.core import exceptions, serializers
from django.db import connection

class models_test(TestCase):
    def test_forms0(self):
        data = {'username': 'testclient',
                    'password1': 'test123',
                    'password2': 'test123',}
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())
