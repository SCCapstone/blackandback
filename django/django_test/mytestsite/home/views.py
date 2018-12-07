from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def index(request):
	all_links = {'upload', 'accounts/login', 'aboutus', 'contact', 'top_photos', 'share'}
	template = loader.get_template('home/index.html')
	context = {
		'all_links' :all_links,
	}
	return HttpResponse(template.render(context, request))

# Create your views here.
def aboutus(request):
	return HttpResponse(render(request, 'home/aboutus.htm'))

def contact(request):
	return HttpResponse(render(request, 'home/contact.htm'))

def top_photos(request):
	#add in way to get top photos obviously
	return HttpResponse(render(request, 'home/top_photos.htm'))
