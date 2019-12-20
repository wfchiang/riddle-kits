from django.http import HttpResponse 
from django.shortcuts import render

def home (http_request): 
    return render(http_request, 'index.html', {})