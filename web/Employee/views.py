from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils import timezone

from Manager.models import Car
from UserAuth.models import UserProfile


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
        ]
        buttons = {
            'CR': [
                {'text': 'Change to Till Worker', 'value': 'change_to_till_worker'},
                {'text': 'Demote to Customer', 'value': 'demote_to_customer'},
            ],
            'TW': [
                {'text': 'Change to Car Retrieval Specialist', 'value': 'change_to_car_retrieval_specialist'},
                {'text': 'Demote to Customer', 'value': 'demote_to_customer'},
            ],
            'CU': [
                {'text': 'Promote to Car Retrieval Specialist', 'value': 'promote_to_car_retrieval_specialist'},
                {'text': 'Promote to Till Worker', 'value': 'promote_to_till_worker'},
            ],
        }
        context["tabs"] = tabs
        context["car_inventory"] = Car.objects.all()
        context["users"] = UserProfile.objects.all()
        context["user_buttons"] = buttons
    else:
        return HttpResponseForbidden("Unauthorized: User not part of staff!")

    return render(request, 'Employee/staff.html', context)
