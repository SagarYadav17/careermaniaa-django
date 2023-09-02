from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

urlpatterns = [
    path("", lambda request: HttpResponse()),
    path("admin/", admin.site.urls),
    path("api/auth/", include("authentication.urls")),
    path("api/core/", include("core.urls")),
]
