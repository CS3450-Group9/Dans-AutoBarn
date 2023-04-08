from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone
from django.contrib import messages
from datetime import datetime, date
from Manager.models import Car
from Customer.models import Reservation
from UserAuth.models import UserProfile

def verify_pickup(request):
    return staff(request, None)

def checkout(request, res_id):
    res = get_object_or_404(Reservation, pk=res_id)
    time_now = timezone.now()
    formatted_date = time_now.strftime("%m-%d-%Y")
    context = {
        'res': res,
        'formatted_date': formatted_date,
    }
    tabname = "CheckoutRes"
    if request.method == 'POST':
        user = res.user
        try:
            if request.POST['insurance']:
                user.balance -= 50
                print("insurance radio button flagged")
                res.car.checked_out = True
                user.save()
                messages.success(request, f"Insurance selected, checked out status: {res.car.checked_out}", extra_tags=tabname)
        except MultiValueDictKeyError:
            res.car.lowjacked = True
            res.car.checked_out = True
            print("no insurance")
            res.save()
            messages.success(request, f"No insurance, checked out status: {res.car.checked_out}", extra_tags=tabname)
        except IntegrityError:
            messages.error(request, "Insufficient Funds.")
            return redirect('/search')
        return redirect("Employee:staff", "CheckoutRes")
            
    return render(request, 'Employee/checkoutRes.html', context)

def staff_default(request):
    return redirect("Employee:staff", "active-rentals")

def staff(request, tab):
    time_now = timezone.now()
    formatted_date = time_now.strftime("%m-%d-%Y")
    today = date.today()
    today_reservations = Reservation.objects.filter(start_date=today)
    return_reservations = Reservation.objects.filter(end_date=today)
    context = {"formatted_date": formatted_date}
    tabs = [
        {"url": "active-rentals",
            "tab_title": "Active Rentals",
            "component_name": "ActiveRentals",
            "template": 'Employee/staffTabs/activeRentals.html' },
        # {"url": "verify",
        #     "tab_title": "Verify Pick-Up",
        #     "component_name": "Verify",
        #     "template": 'Employee/staffTabs/verifyPickup.html' },
        {"url": "broken-cars",
            "tab_title": "Currently Broken Cars",
            "component_name": "BrokenCars",
            "template": 'Employee/staffTabs/brokenCars.html' },
    ]

    if not request.user.is_authenticated:
        context["error"] = "User is not signed in!"

    elif request.user.userprofile.auth_level == "TW" or request.user.userprofile.auth_level == "CR":
        # For now, CR and TW have the same tabs
        tabs += [
            {"url": "log-hours",
             "tab_title": "Log Hours Worked",
             "component_name": "LogHours",
             "template": 'Employee/staffTabs/logHours.html' },
            {"url": "verify",
            "tab_title": "Verify Pick-Up",
            "component_name": "Verify",
            "template": 'Employee/staffTabs/verifyPickup.html' },
            {"url": "verifyDrop",
            "tab_title": "Verify Drop-Off",
            "component_name": "VerifyDrop",
            "template": 'Employee/staffTabs/verifyDropOff.html' },
        ]
        context["tabs"] = tabs
        context["today_reservations"] = today_reservations
        context["return_reservations"] = return_reservations
    elif request.user.userprofile.auth_level == "MA":
        # if tab == "cars" and request == "POST":
        #     return render()
        tabs += [
            {"url": "cars",
             "tab_title": "Manage Cars",
             "component_name": "CarsView",
             "template": 'Manager/managerTabs/manageCars.html' },
            {"url": "users",
             "tab_title": "Manage Users",
             "component_name": "UsersView",
             "template": 'Manager/managerTabs/manageUsers.html' },
            {"url": "hours",
             "tab_title": "Review Hours",
             "component_name": "Hours",
             "template": 'Manager/managerTabs/reviewHours.html' },
            {"url": "verify",
            "tab_title": "Verify Pick-Up",
            "component_name": "Verify",
            "template": 'Employee/staffTabs/verifyPickup.html' },
            {"url": "verifyDrop",
            "tab_title": "Verify Drop-Off",
            "component_name": "VerifyDrop",
            "template": 'Employee/staffTabs/verifyDropOff.html' },
        ]
        context["tabs"] = tabs
        context["today_reservations"] = today_reservations
        context["return_reservations"] = return_reservations
        context["car_inventory"] = Car.objects.all()
        context["users"] = UserProfile.objects.all()
    else:
        return HttpResponseForbidden("Unauthorized: User not part of staff!")

    return render(request, 'Employee/staff.html', context)
