from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("chats/", include("chats.urls")),
]

if settings.DEBUG:
    urlpatterns.append(path("admin/", admin.site.urls))
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
