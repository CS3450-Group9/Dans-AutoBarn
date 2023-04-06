from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import date

from Manager.models import Car
from UserAuth.models import UserProfile
from Customer.models import Reservation


def staff_default(request):
    return redirect("Employee:staff", "active-rentals")

def staff(request, tab):
    time_now = timezone.now()
    formatted_date = time_now.strftime("%m-%d-%Y")
    context = {"formatted_date": formatted_date}
    tabs = [
        {"url": "active-rentals",
            "tab_title": "Active Rentals",
            "component_name": "ActiveRentals",
            "template": 'Employee/staffTabs/activeRentals.html' },
        {"url": "verify",
            "tab_title": "Verify Pick-Up",
            "component_name": "Verify",
            "template": 'Employee/staffTabs/verifyPickup.html' },
        {"url": "broken-cars",
            "tab_title": "Broken Cars",
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
        ]
        context["tabs"] = tabs
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
        ]
        context["tabs"] = tabs
        context["car_inventory"] = Car.objects.all()
        context["users"] = UserProfile.objects.all()
    else:
        return HttpResponseForbidden("Unauthorized: User not part of staff!")

    # handle requests for modifying car fields
    if request.method == "POST":
        if tab == "broken-cars":
            return toggle_low_jacked(request)
        if tab == "active-rentals":
            # decide lowjack or return
            if request.POST.get("button") == "lowjack":
                return toggle_low_jacked(request)
            elif request.POST.get("button") == "return":
                return return_car(request)

    return render(request, 'Employee/staff.html', context)

def toggle_low_jacked(request):
    try: 
        car_id = int(request.POST.get("car_id"))
        car = Car.objects.get(id=car_id)
        car.lowjacked = not car.lowjacked
        car.location = "No Location Yet"
        car.save()
    except:
        print("ERROR")
        pass
    return redirect("Employee:staff", "broken-cars")

def return_car(request):
    try: 
        car_id = int(request.POST.get("car_id"))
        car = Car.objects.get(id=car_id)
        car.checked_out = False
        car.save()
        # delete last reservation
        reservations = Reservation.objects.filter(car=car_id, end_date__lte=date.today())
        reservations.delete()
    except:
        print("ERROR")
        pass
    return redirect("Employee:staff", "active-rentals")