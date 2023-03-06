from django.urls import path, re_path
from . import views

app_name = 'Customer'
urlpatterns = [
    path('profile/balance', views.add_balance, name="balance"),
    re_path(r'^profile/.*', views.profile, name="profile"), # Used regex path to include all paths with the prefix 'profile/'
    path('search/', views.search_for_res, name='search'),
]
