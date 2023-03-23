from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from Customer.models import Reservation
from Manager.models import Car
from .models import Car, Reservation
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


def profile(request, context=dict()):
    tabs = [
        {"url": "info",
         "tab_title": "Personal Information",
         "component_name": "Info",
         "template": 'Customer/profileTabs/personalInfo.html'},
        {"url": "balance",
         "tab_title": "Manage Balance",
         "component_name": "Balance",
         "template": 'Customer/profileTabs/manageBalance.html'},
        {"url": "reservations",
         "tab_title": "Current Reservations",
         "component_name": "Reservations",
         "template": 'Customer/profileTabs/reservations.html'},
        {"url": "pass-change",
         "tab_title": "Change Password",
         "component_name": "PassChange",
         "template": 'Customer/profileTabs/passChange.html'},
        {"url": "car-broke",
         "tab_title": "Car Broken?",
         "component_name": "CarBroken",
         "template": 'Customer/profileTabs/carBroke.html'},
    ]
    if request.user.is_authenticated:
        context.update({"tabs": tabs})
        context.update({ "password_form": PasswordChangeForm(request.user.userprofile.user) })
    else:
        context = {"error": "User is not signed in!"}
    return render(request, 'Customer/profile.html', context)

def add_balance(request):
    if request.method != "POST":
        return profile(request)
    try:
        amount = int(request.POST.get("inputBal", 0))
        if amount < 1: raise ValueError
        request.user.userprofile.balance += amount
        request.user.userprofile.full_clean()
        request.user.userprofile.save()
        context = { "bal_msg": f"Successfully added ${amount} to account!" }
    except ValueError:
        context = { "bal_msg": "Amount must be a positive integer" }
    except:
        context = {"bal_msg": "Something went wrong... Unable to transfer funds."}

    return profile(request, context=context)

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user.userprofile.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
        else:
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, error)
    return profile(request)

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
