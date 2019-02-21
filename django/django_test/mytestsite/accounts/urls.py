from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from . import views
from django.conf import settings
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'), #
]
