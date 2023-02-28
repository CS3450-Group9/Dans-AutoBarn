from django.urls import path
from . import views

app_name = 'Customer'
urlpatterns = [
    path('search', views.search_for_res, name='search'),
]
