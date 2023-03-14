from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from Customer.models import Reservation
from Manager.models import Car

def search_for_res(request):
    time_now = timezone.now()
    formatedDate = time_now.strftime("%m-%d-%Y")
    car_inventory = Car.objects.all()
    context = {
        'formatedDate': formatedDate,
        'car_inventory': car_inventory,
        }
    return render(request, 'Customer/search.html', context)

def create_res(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    time_now = timezone.now()
    formatedDate = time_now.strftime("%m-%d-%Y")
    try: 
        curr_reservations = Reservation.objects.filter(car=car_id)
    except  (KeyError, Reservation.DoesNotExist):
        return render(request, 'Customer/reservation.html', {'car': car})
    else:
        context = {
            'formatedDate': formatedDate,
            'car': car,
            'curr_reservations': curr_reservations,
            }
        return render(request, 'Customer/reservation.html', context)