from django.urls import path, re_path
from . import views

app_name = 'Employee'
urlpatterns = [
    path('staff/<str:tab>/', views.staff, name='staff'),
    path('staff/', views.staff_default, name="staff_default"),
]
