from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import datetime
from .models import Car, Reservation
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST



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
    
    if request.method == "POST":
        try:
            start_date = format_date(request.POST.get("start-date"))
            end_date = format_date(request.POST.get("end-date"))
        except Exception as e:
            print(e)
            messages.error(request, "The date entered was not valid")
            return render(request, 'Customer/reservation.html', context)

        user = request.user.userprofile
        response = check_availability(request, car_id, "dict")
        if not response["available"]:
            messages.error(request, "Reservation not available")
            return render(request, 'Customer/reservation.html', context)

    return render(request, 'Customer/reservation.html', context)

@require_POST
def check_availability(request, car_id, mode="JSONResponse"):
    json = {}
    try:
        start_date = format_date(request.POST.get("start-date"))
        end_date = format_date(request.POST.get("end-date"))
        car = Car.objects.get(pk=car_id)
        price = (end_date - start_date).days * car.get_res_cost()
        json['price'] = price
    except Exception as e:
        print(e)
        json["error_msg"] = "The dates entered are not valid."

    curr_reservations = Reservation.objects.filter(car=car_id)
    json["available"] = True
    for res in curr_reservations:
        if res.check_res_conflict(start_date) or res.check_res_conflict(end_date):
            json["available"] = False
            break

    if mode == "dict": return json
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