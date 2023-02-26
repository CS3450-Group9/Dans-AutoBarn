from django.urls import path, include
from . import views

app_name = 'Customer'
urlpatterns = [
    path('profile/', views.profile, name="profile")
]