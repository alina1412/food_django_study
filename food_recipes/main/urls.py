from django.contrib import admin
from django.urls import path, re_path

from . import views

app_name = "main"


urlpatterns = [
    path("", views.index, name="main"),
    # path('product/<int:a>/details/<int:b>',views.get_demo),
    # path('calc/<int:a>/<slug:operation>/<int:b>',views.calc),
    # path("profile/", views.profile, name="profile"),
    path("foodlist/<int:cat_id>/", views.foodlist, name="foodlist"),
    path("gallery/", views.gallery, name="gallery"),
    path("about/<int:id>/", views.details, name="details"),
    path("contacts/", views.contacts, name="contacts"),
    path("userstop/", views.users_top, name="top"),
    path("add/", views.add_recipe, name="add_rec"), #as_view()
    path("update/<int:pk>/", views.RecipeUpdateView.as_view(), name="rec_update"),
    # path("login/", views.loginView, name="login"),
    
]
