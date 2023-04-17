from django.urls import path
from . import views

app_name = 'Employee'
urlpatterns = [
    path('staff/', views.staff_default, name="staff_default"),
    path('checkoutRes/<int:res_id>', views.checkout, name='checkout'),
    path('staff/<str:tab>/', views.staff, name='staff'),
]
