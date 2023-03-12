from django.shortcuts import render

def employee(request):
    tabs = [
        {"id": "active-rentals",
         "tab_title": "Active Rentals",
         "component_name": "ActiveRentals",
         "template": 'Employee/employeeTabs/activeRentals.html' },
        {"id": "verify",
         "tab_title": "Verify Pick-Up",
         "component_name": "Verify",
         "template": 'Employee/employeeTabs/verifyPickup.html' },
        {"id": "broken-cars",
         "tab_title": "Currently Broken Cars",
         "component_name": "BrokenCars",
         "template": 'Employee/employeeTabs/brokenCars.html' },
    ]
    if not request.user.is_authenticated:
        context = {"error": "User is not signed in!"}
    elif request.user.userprofile.auth_level == "TW" or request.user.userprofile.auth_level == "CR":
        tabs += [
            {"id": "log-hours",
             "tab_title": "Log Hours Worked",
             "component_name": "LogHours",
             "template": 'Employee/employeeTabs/logHours.html' },
            {"id": "pay-history",
             "tab_title": "Pay History",
             "component_name": "PayHistory",
             "template": 'Employee/employeeTabs/payHistory.html' },
        ]
        context = {"tabs": tabs}
    elif request.user.userprofile.auth_level == "MA":
        context = {"tabs": tabs}
    else:
        context = {"error": "User is not an employee!"}

    return render(request, 'Employee/employee.html', context)