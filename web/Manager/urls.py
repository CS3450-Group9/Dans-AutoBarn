from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Manager'
urlpatterns = [
    path('inventory/', views.car_inventory, name='cars'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)