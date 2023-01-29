from django.shortcuts import render
from django.views.generic import TemplateView
import json
from django.http import JsonResponse
from temp.models import Temp

# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"

class CustomerView(TemplateView):
    template_name = "customer.html"

def UserName(request):
    data = json.loads(request.body)

    user_name = data["user-name"]
    print(user_name)

    response = {
        "success": True
    }
    
    return JsonResponse(response)