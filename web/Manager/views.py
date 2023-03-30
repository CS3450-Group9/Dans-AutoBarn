from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError

from .models import Car


def car_inventory(request):
    if request.method != 'POST':
        return redirect("Employee:staff")

    tabname = "cars"
    try:
        car_make = request.POST['car-make']
        car_model = request.POST['car-model']
        car_year = request.POST['car-year']
        car_license = request.POST['car-license']
        car_res_cost = request.POST['car-res-cost']
        car_pic = request.FILES["car-pic"]
        new_car = Car.objects.create(
            make=car_make,
            model=car_model,
            year=car_year,
            gas_fill_percent=100,
            plate_number=car_license,
            image=car_pic,
            lowjacked=False,
            reservation_cost=car_res_cost,
        )
        new_car.save()

    except MultiValueDictKeyError as e:
        print(f"ERROR: {str(e)}")
        messages.error(request, "The request did not include the necessary info.", extra_tags=tabname)
        return redirect("Employee:staff", "cars")

    except (ValueError, IntegrityError) as e:
        print(f"ERROR: {str(e)}")
        messages.error(request, f"Incorrect value in input.", extra_tags=tabname)
        return redirect("Employee:staff", "cars")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        messages.error(request, "An error occurred. Please try again later.", extra_tags=tabname)
        return redirect("Employee:staff", "cars")
        
    messages.success(request, "Successfully added car to inventory!", extra_tags=tabname)
    return redirect("Employee:staff", "cars")