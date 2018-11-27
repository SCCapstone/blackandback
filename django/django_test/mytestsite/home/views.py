from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def index(request):
	all_links = {'upload'}
	template = loader.get_template('home/index.html')
	context = {
		'all_links' :all_links,
	}
	return HttpResponse(template.render(context, request))

# Create your views here.
