from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .recolorMod import recolorNet
from django.http import HttpResponse
from django.core.signals import request_finished
from django.dispatch import receiver


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
		print(uploaded_file_url)
		
	
		fileName = uploaded_file_url
		fileName.replace('\\','/')
		split = fileName.split("/")
		photo = split[4]
		photo = photo.split('.', 1)[0]
		photo = photo + "_recolored.png"
		#filePath = split[0] + "/" + split[1] + "/" + split[2] + "/" + split[3] + "/" +  photo
		filePath = split[1] + "/" + split[2] + "/" + split[3] + "/" +  photo
		print(filePath)
		
		#render(request, 'upload/upload.html',{
		#	'uploaded_file_url':uploaded_file_url
		#})
		#drive_list.upload_photo(filePath)
		
		try:
			return render(request, 'upload/upload.html', {
				'uploaded_file_url': uploaded_file_url
		})#, drive_list.upload_photo(filePath)
		finally:
			request_page(request,filePath)
			print("work")


			#drive_list.upload_photo(filePath)
		
			#drive_list.upload_photo(filePath)
		#return render(request, 'upload/upload.html', {
		#	'uploaded_file_url': uploaded_file_url
		#})
	return render(request, 'upload/upload.html')

@receiver(request_finished)
def my_callback(sender, **kwargs):
	print("Finished", sender)
	
	

def request_page(request,filePath):
	if request.method == 'POST' and filePath:
		print("was this it")
		drive_list.upload_photo(filePath)
#s	return render(request, 'upload/upload.html')
	#if request.method == 'GET':
		#import drive_list
	#	drive_list.upload_photo()
	#return render(request, 'upload/upload.html')
  #if(request.GET.get('mybtn')):
	#  drive_list.upload_photo()
	#  return render(request, 'upload/upload.html')