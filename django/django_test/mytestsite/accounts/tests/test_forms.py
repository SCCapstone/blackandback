# from django.test import TestCase
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# #from .forms import *
# #from .models import *
# class SignUpFormTest(TestCase):
#     def test_form_renders_item_text_input(self):
#         form = SignUpForm()
#         self.fail(form.as_p())
#
# class Setup_Class(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(email="user@mp.com", password="user", first_name="user", phone=12345678)
#
# class User_Creation_Form_Test(TestCase):
#
#     # Valid Form Data
#     def test_UserForm_valid(self):
#         form = UserForm(data={'email': "user@mp.com", 'password': "user", 'first_name': "user", 'phone': 12345678})
#         self.assertTrue(form.is_valid())
#
#     # Invalid Form Data
#     def test_UserForm_invalid(self):
#         form = UserForm(data={'email': "", 'password': "mp", 'first_name': "mp", 'phone': ""})
#         self.assertFalse(form.is_valid())
from django.test import TestCase
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class forms_test(TestCase):
    def test_forms0(self):
        data = {'username': 'testclient',
                    'password1': 'test123',
                    'password2': 'test123',}
        form = UserCreationForm(data)
        self.assertFalse(form.is_valid())

    def test_forms1(self):
        data = {'username': 'Donk',
                    'password1': 'InTimidator23',
                    'password2': 'InTimidator23',}
        form = UserCreationForm(data)
        self.assertTrue(form.is_valid())
    # def test_forms2(self):
    #     data = {'username':'testclient', 'first_name':'allie', 'last_name':'rogers', 'email':'anything@gmail.com', 'password':'123', 'confirmation':'123'}
    #     form = UserCreationForm(data)
    #     form = SignUpForm(form)
    #     self.assertFalse(form.is_valid())
