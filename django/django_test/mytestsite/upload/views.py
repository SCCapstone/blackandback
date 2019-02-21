from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .recolorMod import recolorNet
from django.http import HttpResponse
import os, shutil

username = ''
def upload(request):
	if request.method == 'POST' and request.FILES['myfile']:
		username = request.user.username
		filepath = "upload/files/" + username + "/"
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(username + "/" + myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		recolorNet.runNN(username,myfile.name)
		return render(request, 'upload/upload.html', {
			'uploaded_file_url': uploaded_file_url
		})
	return render(request, 'upload/upload.html')
	
