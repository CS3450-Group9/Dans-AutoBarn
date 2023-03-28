from django.urls import path, re_path
from . import views

app_name = 'Employee'
urlpatterns = [
    path('staff/<str:tab>/', views.staff, name='staff'),
    path('staff/', views.staff_default, name="staff"), # Used regex path to include all paths with the prefix 'employee/'
]
