from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MediaStreamListAV,
    MediaStreamDetailAV,
    ReviewList,
    ReviewDetail,
    UserReview,
    CreateReview,
    StreamPlatformVS,
    MediaStreamList,
)

router = DefaultRouter()
router.register("streams", StreamPlatformVS, basename="stream-platform")

urlpatterns = [
    path("", MediaStreamListAV.as_view(), name="media-list"),
    path("", include(router.urls)),
    path("<int:pk>/", MediaStreamDetailAV.as_view(), name="media-detail"),
    path("<int:pk>/reviews/create/", CreateReview.as_view(), name="create-review"),
    path("<int:pk>/reviews/", ReviewList.as_view(), name="review-list"),
    path("reviews/<int:pk>/", ReviewDetail.as_view(), name="review-detail"),
    path("user-reviews/", UserReview.as_view(), name="user-review-detail"),
    path("new_media/", MediaStreamList.as_view(), name="search-media"),
]
