from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
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
    curr_reservations = Reservation.objects.filter(car=car_id)
    context = {
                'formatedDate': formatedDate,
                'car': car,
                'curr_reservations': curr_reservations,
                }
    if request.method == 'POST':
        input_startDate = request.POST['startDate']
        input_endDate = request.POST['endDate']
        datetime_startDate = get_datetime_object(input_startDate)
        datetime_endDate = get_datetime_object(input_endDate)
        user = request.user.userprofile
        for res in curr_reservations:
            if res.check_res_conflict(datetime_startDate) or res.check_res_conflict(datetime_endDate):
                context['error_message'] = 'Selected dates are unavailable'                
        new_reservation = Reservation(car=car, user=user, startDate=datetime_startDate, endDate=datetime_endDate)
        price = new_reservation.get_num_days() * car.get_res_cost()
        context['input_startDate'] = input_startDate
        context['input_endDate'] = input_endDate
        context['new_reservation'] = new_reservation
        context['price'] = price
        print(request.POST)
        if request.method == 'POST':
            print("Confirm works")
            new_reservation.save()
            return render(request, 'Customer/reservation.html', context)
    return render(request, 'Customer/reservation.html', context)

def confirm_res(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    time_now = timezone.now()
    formatedDate = time_now.strftime("%m-%d-%Y")
    context = {
        'formatedDate': formatedDate,
        'reservation': reservation,
        }
    return render(request, 'Customer/confirmation.html', context)

def get_datetime_object(date_string):
    year = date_string[:4]
    month = date_string[5:7]
    day = date_string[8:10]
    year = int(year)
    month = int(month)
    day = int(day)
    date = datetime(year, month, day)
    date = datetime.date(date)
    return date
