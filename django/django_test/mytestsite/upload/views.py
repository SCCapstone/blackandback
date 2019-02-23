from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .recolorMod import recolorNet
from django.http import HttpResponse
import os, shutil
import drive_list

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
		drive_list.upload_photo()
		return render(request, 'upload/upload.html', {
			'uploaded_file_url': uploaded_file_url
		})
	return render(request, 'upload/upload.html')

def request_page(request):
	if request.method == 'GET':
		drive_list.upload_photo()
	return render(request, 'upload/upload.html')
	#if request.method == 'GET':
		#import drive_list
	#	drive_list.upload_photo()
	#return render(request, 'upload/upload.html')
  #if(request.GET.get('mybtn')):
	#  drive_list.upload_photo()
	#  return render(request, 'upload/upload.html')