from django.shortcuts import render, redirect
from django.contrib import messages
from Manager.models import Car

def staff_default(request):
    return redirect("staff/active-rentals")


def staff(request, tab):
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
         "tab_title": "Currently Broken Cars",
         "component_name": "BrokenCars",
         "template": 'Employee/staffTabs/brokenCars.html' },
    ]
    if not request.user.is_authenticated:
        context = {"error": "User is not signed in!"}
    elif request.user.userprofile.auth_level == "TW" or request.user.userprofile.auth_level == "CR":
        tabs += [
            {"url": "log-hours",
             "tab_title": "Log Hours Worked",
             "component_name": "LogHours",
             "template": 'Employee/staffTabs/logHours.html' },
        ]
        context = {"tabs": tabs}
    elif request.user.userprofile.auth_level == "MA":
        if tab == "cars" and request == "POST":
            try:
                car_make = request.POST['car-make']
                car_model = request.POST['car-model']
                car_year = request.POST['car-year']
                car_license = request.POST['car-license']
                car_res_cost = request.POST['car-res-cost']
            except ValueError:
                messages.error(request, "Incorrectly formatted inputs.")
                return render(request, 'Employee/staff.html', context)
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
            return render(request, 'Employee/staff.html', context)
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
        context = {
            "tabs": tabs,
            "car_inventory": Car.objects.all()
        }
    else:
        context = {"error": "User is not part of staff!"}

    return render(request, 'Employee/staff.html', context)