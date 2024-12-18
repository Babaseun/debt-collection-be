from django.urls import path
from . import views


urlpatterns = [
    path('upload', views.save_csv_data),
    path('', views.get_accounts),
]