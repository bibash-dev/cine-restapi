from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin-dashboard/", admin.site.urls),
    path("api/cine/", include("cineshelf_app.api.urls")),
    path("api/account/", include("user_app.api.urls")),
]
