from django.urls import path, re_path
from . import views

app_name = 'Customer'
urlpatterns = [
    re_path(r'^profile/.*', views.profile, name="profile"),
    path('search/', views.search_for_res, name='search'),
]
