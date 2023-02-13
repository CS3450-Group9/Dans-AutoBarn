from django.urls import path
from . import views

app_name = 'UserAuth'
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('signup', views.signup, name='signup'),
]