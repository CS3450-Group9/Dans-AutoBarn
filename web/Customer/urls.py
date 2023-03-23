from django.urls import path, re_path
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Customer'
urlpatterns = [
    # path('profile/balance', views.add_balance, name="balance"),
    # re_path(r'^profile/.*', views.profile, name="profile"), # Used regex path to include all paths with the prefix 'profile/'
    path('search/', views.search_for_res, name='search'),
    path('<int:car_id>/', views.create_res, name='reservation'),
    path('<int:reservation_id>/', views.confirm_res, name='confirmation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
