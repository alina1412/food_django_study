from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="recipies"),
    # path('product/<int:a>/details/<int:b>',views.get_demo),
    # path('calc/<int:a>/<slug:operation>/<int:b>',views.calc),
    path("about/", views.details, name="details"),
    # path("foodlist/", views.foodlist, name="foodlist"),
    # path("contacts/", views.contacts, name="contacts"),
    # path("sidebar/", views.sidebar, name="sidebar"),
]
