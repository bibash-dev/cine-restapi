from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cine/", include("cineshelf_app.api.urls")),
]
