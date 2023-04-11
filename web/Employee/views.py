from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone
from django.contrib import messages
<<<<<<< HEAD
from datetime import date

=======
from datetime import datetime, date
>>>>>>> dev
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
                res.car.checked_out = True
                user.save()
                res.car.save()
                print(f"Checked out status: {res.car.checked_out}")
                messages.success(request, "Reservation has been checked out!", extra_tags=tabname)
        except MultiValueDictKeyError:
            res.car.lowjacked = True
            res.car.checked_out = True
            print(f"Checked out status: {res.car.checked_out}")
            user.save()
            res.car.save()
            messages.success(request, "Reservation has been checked out!", extra_tags=tabname)
        except IntegrityError:
            messages.error(request, "Insufficient Funds.")
            return redirect('/search')
        return redirect("Employee:staff", "CheckoutRes")
            
    return render(request, 'Employee/checkoutRes.html', context)

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
        "car_inventory": car_inventory}
    tabs = [
        {
            "url": "active-rentals",
            "tab_title": "Active Rentals",
            "component_name": "ActiveRentals",
            "template": 'Employee/staffTabs/activeRentals.html' },
        {"url": "broken-cars",
            "tab_title": "Currently Broken Cars",
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
        context["today_reservations"] = today_reservations
        context["return_reservations"] = return_reservations
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
                {"text": "Demote to Till Worker", "value": "TW"},
                {"text": "Demote to Car Retrieval Specialist", "value": "CR"},
                {"text": "Demote to Customer", "value": "CU"},
            ],
            "CR": [
                {"text": "Promote to Manager", "value": "MA"},
                {"text": "Change to Till Worker", "value": "TW"},
                {"text": "Demote to Customer", "value": "CU"},
            ],
            "TW": [
                {"text": "Promote to Manager", "value": "MA"},
                {"text": "Change to Car Retrieval Specialist", "value": "CR"},
                {"text": "Demote to Customer", "value": "CU"},
            ],
            "CU": [
                {"text": "Promote to Manager", "value": "MA"},
                {"text": "Promote to Car Retrieval Specialist", "value": "CR"},
                {"text": "Promote to Till Worker", "value": "TW"},
            ]
        }
        users_data = []
        for user in UserProfile.objects.all():
            users_data += [{
                "user_profile": user,
                "buttons": user_buttons.get(user.auth_level)
            }]

        context["tabs"] = tabs
        context["today_reservations"] = today_reservations
        context["return_reservations"] = return_reservations
        context["car_inventory"] = Car.objects.all()
        context["users_data"] = users_data 
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
        elif tab=="log-hours":
            return log_hours(request, tab)

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
        car.save()
        # delete last reservation
        reservations = Reservation.objects.filter(car=car_id, end_date__lte=date.today())
        reservations.delete()
    except:
        print("ERROR")
        pass
    return redirect("Employee:staff", "active-rentals")

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