from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import datetime
from .models import Car, Reservation
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q


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
    formattedDate = time_now.strftime("%m-%d-%Y")
    curr_reservations = Reservation.objects.filter(car=car_id)
    context = {
        'formattedDate': formattedDate,
        'car': car,
        'curr_reservations': curr_reservations,
    }
    return render(request, 'Customer/reservation.html', context)

def check_availability(request):
    json = {}
    try:
        car_id = int(request.GET["carID"])
        car = Car.objects.get(pk=car_id)
        start_date = format_date(request.GET["start"])
        end_date = format_date(request.GET["end"])
        timedelta = (end_date - start_date).days + 1
        if timedelta <= 0:
            raise ValueError("End date cannot be before start date.")
        elif timedelta > 50:
            raise ValueError("Cannot reserve a car for more than 50 days.")
        price = timedelta * car.get_res_cost()
        json['price'] = price
    except ValueError as e:
        json["error"] = str(e)
        return JsonResponse(json)
    except MultiValueDictKeyError:
        json["error"] = "Request must contain parameters 'carID', 'start', and 'end'."
        return JsonResponse(json)
    except Car.DoesNotExist:
        json["error"] = f"Car with ID '{car_id}' does not exist."
        return JsonResponse(json)
    except Exception as e:
        # print(e)
        json["error"] = "Something went wrong."
        return JsonResponse(json)

    json["available"] = res_available(car_id, start_date, end_date)
    return JsonResponse(json)

def confirm_res(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    time_now = timezone.now()
    formatedDate = time_now.strftime("%m-%d-%Y")
    context = {
        'formatedDate': formatedDate,
        'reservation': reservation,
        }
    return render(request, 'Customer/confirmation.html', context)

def format_date(date: str):
    date_format = "%Y-%m-%d"
    date_obj = datetime.strptime(date, date_format).date()
    return date_obj

def res_available(car_id, start_date, end_date):
    overlapping = Reservation.objects.filter(
        car_id = car_id,
        end_date__gte=start_date,
        start_date__lte=end_date
    )
    return not overlapping.exists()