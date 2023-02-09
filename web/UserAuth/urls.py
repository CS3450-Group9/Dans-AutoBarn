from django.urls import path

from . import views

app_name = 'UserAuth'
urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup')
]