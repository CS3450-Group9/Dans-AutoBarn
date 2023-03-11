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
    res_date = Reservation.objects.all()
    context = {
        'formatedDate': formatedDate,
        'car': car,
        'res_date': res_date,
        }
    return render(request, 'Customer/reservation.html', context)

# def all_current_res(request, car_id):
#     car = get_object_or_404(Car, pk=car_id)
#     res_list = Reservation.objects.get(pk=car)