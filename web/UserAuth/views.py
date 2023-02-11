from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'UserAuth/home.html')

def login(request):
    # TODO: IMPLEMENT: Query DB for info about the user, redirect to a home page if user authenticated, else give error message
    return render(request, 'UserAuth/login.html')

def signup(request):
    # TODO: IMPLEMENT: Query DB for info about the user, redirect to login/home if user created successfully, else give error message
    return render(request, 'UserAuth/signup.html')
