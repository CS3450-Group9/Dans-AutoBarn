from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Manager'
urlpatterns = [
    path('inventory/', views.car_inventory, name='inventory'),
    path('managerTabs/manageCars', views.car_inventory, name='manageCars')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)