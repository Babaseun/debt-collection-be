from django.urls import path
from . import views


urlpatterns = [
    path("upload", views.save_csv),
    path("", views.get_accounts, name="get_accounts"),
]
