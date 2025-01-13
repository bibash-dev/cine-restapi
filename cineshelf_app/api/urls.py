from django.urls import path
from .views import (
    StreamPlatformListAV,
    StreamPlatformDetailAV,
    MediaStreamListAV,
    MediaStreamDetailAV,
)

urlpatterns = [
    path("streams/", StreamPlatformListAV.as_view(), name="platform-list"),
    path(
        "streams/<int:pk>/",
        StreamPlatformDetailAV.as_view(),
        name="platform-detail",
    ),
    path("media_list/", MediaStreamListAV.as_view(), name="media-list"),
    path("<int:pk>/", MediaStreamDetailAV.as_view(), name="media-detail"),
]
