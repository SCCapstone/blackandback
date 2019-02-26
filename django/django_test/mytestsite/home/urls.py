from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$' , views.index, name='index'),
	url('aboutus', views.aboutus, name='aboutus'),
	url('contact', views.contact, name='contact'),
	url('top_photos', views.top_photos, name='top_photos'),
	url(r'^profile', views.profile, name='profile'),

]
