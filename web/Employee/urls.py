from django.urls import path, re_path
from . import views

app_name = 'Employee'
urlpatterns = [
    re_path(r'^staff/.*', views.staff, name="staff"), # Used regex path to include all paths with the prefix 'employee/'
]
