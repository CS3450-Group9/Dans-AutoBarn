from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
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
    if request.method == 'POST':
        try:
            car_make = request.POST['car-make']
            car_model = request.POST['car-model']
            car_year = request.POST['car-year']
            car_license = request.POST['car-license']
            car_res_cost = request.POST['car-res-cost']
        except ValueError:
            messages.error(request, "Incorrectly formatted inputs.")
            return render(request, 'Manager/managerTabs/manageCars.html', context)
        new_car = Car.objects.create(
            make=car_make,
            model=car_model,
            year=car_year,
            gas_fill_percent=100,
            plate_number=car_license,
            image='cars/placeholder-car.png',
            lowjacked=False,
            reservation_cost=car_res_cost,
        )
        new_car.save()
        return render(request, 'Manager/managerTabs/manageCars.html', context)
    return render(request, 'Manager/managerTabs/manageCars.html', context)