from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    return HttpResponse("Hello world we have login")

def signup(request):
    return HttpResponse("Hello world we have signup")