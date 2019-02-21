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
