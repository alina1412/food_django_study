from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

# from main.views import f_404

handler404 = 'main.views.not_found_view'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("recipes/", include('recipes.urls')),
    path("", include('main.urls')),
    
    # path("home/", include('home.urls')),
] # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
