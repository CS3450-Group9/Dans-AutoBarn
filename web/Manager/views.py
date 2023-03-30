from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError

from .models import Car


def car_inventory(request):
    time_now = timezone.now()
    formattedDate = time_now.strftime("%m-%d-%Y")
    car_inventory = Car.objects.all()
    context = {
        'formattedDate': formattedDate,
        'car_inventory': car_inventory,
    }

    if request.method != 'POST':
        return redirect("Employee:staff")

    try:
        car_make = request.POST['car-make']
        car_model = request.POST['car-model']
        car_year = request.POST['car-year']
        car_license = request.POST['car-license']
        car_res_cost = request.POST['car-res-cost']
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

    except MultiValueDictKeyError as e:
        messages.error(request, "POST did not include necessary info.")
        return redirect("Employee:staff", "cars")

    except (ValueError, IntegrityError) as e:
        messages.error(request, f"Incorrect value in input '{e}'")
        return redirect("Employee:staff", "cars")

    except Exception as e:
        print("ERROR: " + e)
        messages.error(request, "An error occurred. Please try again later.")

    return redirect("Employee:staff", "cars")