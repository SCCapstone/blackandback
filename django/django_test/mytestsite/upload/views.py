from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .recolorMod import recolorNet
from django.http import HttpResponse
import os, shutil


def clearDirs():
	for filename in os.listdir('upload/files/'):
		os.remove('upload/files/' + filename)
def upload(request):
	if request.method == 'POST' and request.FILES['myfile']:
		clearDirs()
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		recolorNet.runNN()
		return render(request, 'upload/upload.html', {
			'uploaded_file_url': uploaded_file_url
		})
	return render(request, 'upload/upload.html')