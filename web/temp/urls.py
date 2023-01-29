from django.urls import path
from temp.views import HomeView, CustomerView

app_name = 'temp'
urlpatterns = [
    path('', HomeView.as_view(), name='homepage'),
    path('customer', CustomerView.as_view(), name='customer')
]