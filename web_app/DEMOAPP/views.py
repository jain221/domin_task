from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def hi(request):
    return (render(request,'DEMOAPP/dashboard.html'))
# def hi(request):
#     return HttpResponse('<h1> This is my home page </h1>')
