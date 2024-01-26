"""
This file serves as the main URL configuration for the project settings. All dependent URLs are organized within their
respective modules, promoting a modular and maintainable structure. In this configuration, the 'admin/' endpoint is
reserved for Django's admin interface, and the 'api/' endpoint is delegated to the 'api_task.urls' module,
encapsulating the API-related routes. This modular approach enhances code organization and readability, making it easier
to manage and extend the project's URL structure.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from api_task.views import login_view, dashboard_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', login_view, name='user-login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path("api/", include("api_task.urls"))
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
