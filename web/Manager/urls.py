from django.urls import path
from . import views

app_name = 'Manager'
urlpatterns = [
    path('inventory/', views.car_inventory, name='cars'),
    path('removeCar/<int:car_id>', views.remove_car, name='remove'),
]