from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Customer'
urlpatterns = [
    path('profile/pass-change/', views.password_change, name="pass_change"),
    path('profile/balance/', views.add_balance, name="balance"),
    re_path(r'^profile/.*', views.profile, name="profile"),
    path('search/', views.search_for_res, name='search'),
    path('cars/<int:car_id>/', views.create_res, name='reservation'),
    path('check-availability/', views.availability_api, name='availability'),
    path('confirm/<str:token>/', views.confirm_res, name='confirmation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
