from django.shortcuts import render
from django.utils import timezone
from .models import Car

def profile(request):
    return render(request, 'Customer/profile.html')

def search_for_res(request):
    time_now = timezone.now()
    formatedDate = time_now.strftime("%m-%d-%Y")
    car_inventory = Car.objects.all()
    context = {
        'formatedDate': formatedDate,
        'car_inventory': car_inventory,
        }
    return render(request, 'Customer/search.html', context)
