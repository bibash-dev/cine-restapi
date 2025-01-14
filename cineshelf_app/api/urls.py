from django.urls import path
from .views import (
    StreamPlatformListAV,
    StreamPlatformDetailAV,
    MediaStreamListAV,
    MediaStreamDetailAV,
    ReviewList,
    ReviewDetail,
    CreateReview,
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
    # path("reviews/", ReviewList.as_view(), name="review-list"),
    # path("reviews/<int:pk>/", ReviewDetail.as_view(), name="review-detail"),
    path("media/<int:pk>/create-review", CreateReview.as_view(), name="create-review"),
    path("media/<int:pk>/reviews", ReviewList.as_view(), name="review-list"),
    path("media/reviews/<int:pk>", ReviewDetail.as_view(), name="review-detail"),
]
