from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('profile', views.profile, name = 'profile'),
    path('top_photos', views.top_photos, name = 'top_photos'),
    path('aboutus', views.aboutus, name = 'aboutus'),
    path('contact', views.contact, name = 'contact'),
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]