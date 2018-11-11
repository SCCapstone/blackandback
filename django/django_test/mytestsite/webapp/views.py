from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, welcome to the blackandback page")

def home(request):
    return render(request, 'webapp/base.html')

