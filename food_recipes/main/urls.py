from django.contrib import admin
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="main"),
    # path('product/<int:a>/details/<int:b>',views.get_demo),
    # path('calc/<int:a>/<slug:operation>/<int:b>',views.calc),
    path("profile/", views.profile, name="profile"),
    path("foodlist/", views.foodlist, name="foodlist"),
    path("about/<int:id>/", views.details, name="details"),
    # path("contacts/", views.contacts, name="contacts"),
    path("sidebar/", views.sidebar, name="sidebar"),
]
