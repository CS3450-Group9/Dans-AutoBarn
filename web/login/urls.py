from django.urls import path
from login.views import LoginView

from . import views

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
]
