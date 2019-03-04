from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

import glob
import logging
import os
import re


def index(request):
	all_links = {'upload', 'accounts/login', 'aboutus', 'contact', 'featured_photos', 'share'}
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

def featured_photos(request):
	#add in way to get top photos obviously
	users = User.objects.all()
	your_media_root = settings.MEDIA_ROOT
	base_url = settings.BASE_DIR
	#listing = os.listdir(os.path.join(base_url,your_media_root))
	#your_path = os.path.join(base_url,your_media_root)
	print("Path: ", your_media_root)
	recoloredList = []
	for path, dirs, files in os.walk(your_media_root):
		print(path)
		print("Subdirectories: ", dirs)
		print(files)
		for file in files:
			if file.endswith(".png"):
				recoloredList.append(file)
	print("RECOLORED LIST: ", recoloredList)
	#f fileName.endswith(".png"):
	#	print("Display this image")
			
	template = loader.get_template('home/featured_photos.htm')
	context = {
        'users': users,
		'your_media_root': your_media_root,
		'recoloredList' : recoloredList,
		
    }
	return HttpResponse(template.render(context, request))
	#return HttpResponse(render(request, 'home/featured_photos.htm'))
