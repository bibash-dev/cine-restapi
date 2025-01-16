from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    # StreamPlatformListAV,
    # StreamPlatformDetailAV,
    MediaStreamListAV,
    MediaStreamDetailAV,
    ReviewList,
    ReviewDetail,
    UserReview,
    CreateReview,
    StreamPlatformVS,
    MediaStreamList,
)
from ..models import MediaStream

router = DefaultRouter()
router.register("streams", StreamPlatformVS, basename="stream-platform")

urlpatterns = [
    path("", include(router.urls)),
    # path("streams/", StreamPlatformListAV.as_view(), name="platform-list"),
    # path(
    #     "streams/<int:pk>/",
    #     StreamPlatformDetailAV.as_view(),
    #     name="platform-detail",
    # ),
    path("media_list/", MediaStreamListAV.as_view(), name="media-list"),
    path("<int:pk>/", MediaStreamDetailAV.as_view(), name="media-detail"),
    # path("reviews/", ReviewList.as_view(), name="review-list"),
    # path("reviews/<int:pk>/", ReviewDetail.as_view(), name="review-detail"),
    path("<int:pk>/create_review/", CreateReview.as_view(), name="create-review"),
    path("<int:pk>/reviews/", ReviewList.as_view(), name="review-list"),
    path("reviews/<int:pk>/", ReviewDetail.as_view(), name="review-detail"),
    # path("reviews/<str:username>/", UserReview.as_view(), name="user-review-detail"),
    path("reviews/", UserReview.as_view(), name="user-review-detail"),
    path("new_media/", MediaStreamList.as_view(), name="search-media"),
]
