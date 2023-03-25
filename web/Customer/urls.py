from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Customer'
urlpatterns = [
    path('profile/<str:tab>/', views.profile, name='profile'),
    path('profile/', views.profile_default, name='profile'),
    path('search/', views.search_for_res, name='search'),
    path('cars/<int:car_id>/', views.create_res, name='reservation'),
    path('check-availability/', views.availability_api, name='availability'),
    path('confirm/<str:token>/<int:res_id>/', views.confirm_res, name='confirmation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
