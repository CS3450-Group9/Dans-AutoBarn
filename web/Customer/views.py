from django.shortcuts import render
from django.utils import timezone
from .models import Car

def profile(request, context={}):
    return render(request, 'Customer/profile.html', context)

def add_balance(request):
    if request.method != "POST":
        return profile(request)
    try:
        # For now, we will just deal with integers
        amount = int(request.POST.get("inputBal", 0))
        if amount <= 0: raise ValueError
    except ValueError:
        context = { "msg": "Amount must be a positive integer" }
        return profile(request, context=context)

    try:
        request.user.userprofile.balance += amount
        request.user.userprofile.save()
        context = { "msg": f"Successfully added ${amount} to account!" }
    except:
        context = {"msg": "Something went wrong... Unable to transfer funds."}

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
