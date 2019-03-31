from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$' , views.index, name='index'),
	url('aboutus', views.aboutus, name='aboutus'),
	url('contact', views.contact, name='contact'),
	url('featured_photos', views.featured_photos, name='featured_photos'),
	url(r'^profile', views.profile, name='profile'),
	url('stats', views.stats, name='stats'),
]
