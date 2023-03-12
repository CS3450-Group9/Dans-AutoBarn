from django.shortcuts import render
from django.utils import timezone
from .models import Car

def profile(request, context=dict()):
    tabs = [
        {"id": "info",
         "tab_title": "Personal Information",
         "component_name": "Info",
         "template": 'Customer/profileTabs/personalInfo.html'},
        {"id": "balance",
         "tab_title": "Manage Balance",
         "component_name": "Balance",
         "template": 'Customer/profileTabs/manageBalance.html'},
        {"id": "reservations",
         "tab_title": "Current Reservations",
         "component_name": "Reservations",
         "template": 'Customer/profileTabs/reservations.html'},
        {"id": "pass-change",
         "tab_title": "Change Password",
         "component_name": "PassChange",
         "template": 'Customer/profileTabs/passChange.html'},
        {"id": "car-broke",
         "tab_title": "Car Broken?",
         "component_name": "CarBroken",
         "template": 'Customer/profileTabs/carBroke.html'},
    ]
    if request.user.is_authenticated:
        context.update({"tabs": tabs})
    else:
        {"error": "User is not signed in!"}
    return render(request, 'Customer/profile.html', context)

def add_balance(request):
    if request.method != "POST":
        return profile(request)
    try:
        # For now, we will just deal with integers
        amount = int(request.POST.get("inputBal", 0))
        if amount <= 0: raise ValueError
    except ValueError:
        context = { "bal_msg": "Amount must be a positive integer" }
        return profile(request, context=context)

    try:
        request.user.userprofile.balance += amount
        request.user.userprofile.save()
        context = { "bal_msg": f"Successfully added ${amount} to account!" }
    except:
        context = {"bal_msg": "Something went wrong... Unable to transfer funds."}

    return profile(request, context=context)

def search_for_res(request):
    time_now = timezone.now()
    formatedDate = time_now.strftime("%m-%d-%Y")
    car_inventory = Car.objects.all()
    context = {
        'formatedDate': formatedDate,
        'car_inventory': car_inventory,
        }
    return render(request, 'Customer/search.html', context)
