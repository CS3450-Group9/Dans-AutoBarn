from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def home(request):
    return render(request, 'UserAuth/home.html')

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {"form": form})

def logout(request):
    return render(request, '/home')
