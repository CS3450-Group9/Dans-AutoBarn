from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Car
from Customer.models import Reservation

def car_inventory(request):
    time_now = timezone.now()
    formattedDate = time_now.strftime("%m-%d-%Y")
    car_inventory = Car.objects.all()
    context = {
        'formattedDate': formattedDate,
        'car_inventory': car_inventory,
    }
    return render(request, 'Manager/inventory.html', context)