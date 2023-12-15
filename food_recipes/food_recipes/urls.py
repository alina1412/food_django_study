from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include


handler404 = 'main.views.not_found_view'


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("recipes/", include('recipes.urls')),
    path("users/", include('users.urls')),
    path("", include('main.urls')),
    
    # path("home/", include('home.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns=[
        path('__debug/__', include(debug_toolbar.urls)),
    ]+ urlpatterns
    
    urlpatterns+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Панель администрирования сайта"
