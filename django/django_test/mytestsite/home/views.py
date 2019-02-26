from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import logging
import os

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

def profile(request):
	if request.method == 'POST' and request.FILES['myfile']:
		filepath = "profile/files/"
		if not os.path.exists(filepath):
			os.makedirs(filepath)
		logging.error("filepath={}".format(filepath))
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		logging.error(str(myfile.name))
		logging.error(myfile)
		filename = fs.save("{}_profile.jpg".format(request.user), myfile)
		uploaded_file_url = str(request.user) + fs.url(filename)
		return render(request, 'home/profile.htm', {
			'uploaded_file_url': uploaded_file_url,
			'profile_url': "/upload/files/{}_profile.jpg".format(request.user)
		})
	elif os.path.exists("upload/files/{}_profile.jpg".format(request.user)):
		return render(request, 'home/profile.htm',
		{'profile_url': "/upload/files/{}_profile.jpg".format(request.user)})
	else:
		return HttpResponse(render(request, 'home/profile.htm'))

def contact(request):
	return HttpResponse(render(request, 'home/contact.htm'))

def top_photos(request):
	#add in way to get top photos obviously
	return HttpResponse(render(request, 'home/top_photos.htm'))
