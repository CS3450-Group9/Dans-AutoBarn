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


def staff_default(request):
    return redirect("Employee:staff", "active-rentals")

def staff(request, tab):

    time_now = datetime.now()
    formatted_date = time_now.strftime("%m-%d-%Y")
    today = date.today()
    today_reservations = Reservation.objects.filter(start_date=today)
    return_reservations = Reservation.objects.filter(end_date=today)
    car_inventory = Car.objects.all()
    context = {
        "formatted_date": formatted_date,
        "car_inventory": car_inventory,
        "today_reservations": today_reservations,
        "return_reservations": return_reservations,
    }
    tabs = [
        {
            "url": "active-rentals",
            "tab_title": "Active Rentals",
            "component_name": "ActiveRentals",
            "template": 'Employee/staffTabs/activeRentals.html' },
        {"url": "broken-cars",
            "tab_title": "Broken Cars",
            "component_name": "BrokenCars",
            "template": 'Employee/staffTabs/brokenCars.html'
        },
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
        ]
        context["tabs"] = tabs
    elif request.user.userprofile.auth_level == "MA":
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
        ]
        user_buttons = {
            "MA": [
                {"text": "Till Worker", "value": "TW"},
                {"text": "Car Retrieval Specialist", "value": "CR"},
                {"text": "Customer", "value": "CU"},
            ],
            "CR": [
                {"text": "Manager", "value": "MA"},
                {"text": "Till Worker", "value": "TW"},
                {"text": "Customer", "value": "CU"},
            ],
            "TW": [
                {"text": "Manager", "value": "MA"},
                {"text": "Car Retrieval Specialist", "value": "CR"},
                {"text": "Customer", "value": "CU"},
            ],
            "CU": [
                {"text": "Manager", "value": "MA"},
                {"text": "Car Retrieval Specialist", "value": "CR"},
                {"text": "Till Worker", "value": "TW"},
            ]
        }
        users_data = []
        for user in UserProfile.objects.all():
            users_data += [{
                "user_profile": user,
                "buttons": user_buttons.get(user.auth_level)
            }]

        context["tabs"] = tabs
        context["car_inventory"] = Car.objects.all()
        context["users_data"] = users_data 
        context["employees"] = UserProfile.objects.filter(auth_level="TW", hours_worked__gte=1) | UserProfile.objects.filter(auth_level="CR", hours_worked__gte=1)
    else:
        return HttpResponseForbidden("Unauthorized: User not part of staff!")

    # handle requests for modifying car fields
    if request.method == "POST":
        if tab == "broken-cars":
            return toggle_low_jacked(request)
        elif tab == "active-rentals":
            # decide lowjack or return
            if request.POST.get("button") == "lowjack":
                return toggle_low_jacked(request)
            elif request.POST.get("button") == "return":
                return return_car(request)
        elif tab == "users":
            return change_user_auth_level(request)
        elif tab == "log-hours":
            return log_hours(request, tab)
        elif tab == "hours":
            return pay_employees(request, tab)

    return render(request, 'Employee/staff.html', context)

def change_user_auth_level(request):
    if request.user.userprofile.auth_level != "MA":
        return HttpResponseForbidden("You do not have permission!")
    try:
        user_id = int(request.POST.get("user_id"))
        user_to_change = UserProfile.objects.get(id=user_id)
        user_to_change.auth_level = request.POST.get("new_auth_level")
        user_to_change.save()
        return redirect("Employee:staff", "users")
    except UserProfile.DoesNotExist:
        return HttpResponseForbidden("User with id '{user}' does not exist!")
    except ValueError:
        return HttpResponseForbidden("Invalid user id!")
    except:
        return HttpResponseForbidden("Bad request")

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
        car.lowjacked = False
        car.save()
        # delete last reservation
        reservations = Reservation.objects.filter(car=car_id, end_date__lte=date.today())
        reservations.delete()
    except:
        print("ERROR")
        pass
    return redirect("Employee:staff", "active-rentals")

def verify_pickup(request):
    return staff(request, None)

def checkout(request, res_id):
    tabname = "verify"
    res = get_object_or_404(Reservation, pk=res_id)
    if request.method == 'POST':
        user = res.user
        car = res.car
        try:
            if request.POST.get('insurance') and not car.checked_out:
                user.balance -= 50
                user.save()
            car.checked_out = True
            car.save()
            messages.success(request, "Reservation has been checked out!", extra_tags=tabname)
        except IntegrityError:
            messages.error(request, "Insufficient Funds.", extra_tags=tabname)
            return redirect('/search')
        return redirect("Employee:staff", "verify")
            
    time_now = timezone.now()
    formatted_date = time_now.strftime("%m-%d-%Y")
    return render(request, 'Employee/checkoutRes.html', {"res": res, "formatted_date": formatted_date})

def log_hours(request, tabname):
    try:
        amount = int(request.POST.get("inputHours", 0))
        if amount < 1: raise ValueError
        request.user.userprofile.hours_worked += amount
        request.user.userprofile.full_clean()
        request.user.userprofile.save()
        messages.success(request, f"Successfully logged {amount} hours!", extra_tags=tabname)
    except ValueError:
        messages.error(request, "Amount must be a positive integer", extra_tags=tabname)
    except:
        messages.error(request, "Something went wrong... Unable to log hours.", extra_tags=tabname)

    return redirect('Employee:staff', tabname)

def pay_employees(request, tabname):
    if request.user.userprofile.auth_level != "MA":
        return redirect('Employee:staff_default')
    PAY_PER_HOUR = 15
    manager = request.user.userprofile
    try:
        employee_id = int(request.POST.get("employee_id"))
        employee = UserProfile.objects.get(id=employee_id)
        pay = employee.hours_worked * PAY_PER_HOUR

        # Subtract pay from current account
        manager.balance -= pay
        manager.full_clean()
        manager.save()
        
        # Add pay to employee account
        employee.balance += pay
        employee.hours_worked = 0
        employee.full_clean()
        employee.save()

        messages.success(request, f"Successfully paid employee!", extra_tags=tabname)
    except UserProfile.DoesNotExist:
        messages.error(request, "Employee with that ID does not exist.", extra_tags=tabname)
    except MultiValueDictKeyError:
        messages.error(request, "Employee ID not provided.", extra_tags=tabname)
    except IntegrityError:
        messages.error(request, "Insufficient Funds.", extra_tags=tabname)
    except:
        messages.error(request, "Something went wrong... Unable to pay employee.", extra_tags=tabname)

    return redirect('Employee:staff', tabname)
    