from django.contrib import admin
from django.urls import path, re_path

from . import views

app_name = "users"

urlpatterns = [
    path("<int:pk>/", views.AccountDetailView.as_view(), name="user"),
    path("user/<int:pk>/", views.UserAccountView.as_view(), name="account"),
    # path("about/<int:id>/", views.details, name="details"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.loginView, name="login"),
    
]
