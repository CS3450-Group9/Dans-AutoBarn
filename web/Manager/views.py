from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError

from .models import Car
from Customer.models import Reservation

def remove_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    curr_reservations = Reservation.objects.filter(car=car_id)
    time_now = timezone.now()
    formatted_date = time_now.strftime("%m-%d-%Y")
    context = {
        'car': car,
        'curr_reservations': curr_reservations,
        'formatted_date': formatted_date,
    }
    tabname = "cars"
    if request.method == 'POST':
        if curr_reservations is None:
            car.delete()
        else:
            curr_reservations.delete()
            car.delete()
            messages.success(request, "Successfully removed car from inventory!", extra_tags=tabname)
            return redirect("Employee:staff", "cars")
            
    return render(request, 'Manager/remove.html', context)

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