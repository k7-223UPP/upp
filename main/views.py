from django.http import HttpResponseRedirect
from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')

