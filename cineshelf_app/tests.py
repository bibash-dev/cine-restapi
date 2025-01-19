from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient, force_authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from cineshelf_app import models


class BaseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="bibash", email="bibash@cine.com", password="bibash123"
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access = str(self.refresh.access_token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

        self.stream_platform = models.StreamPlatform.objects.create(
            name="Netflix",
            description="Netflix is the largest online streaming platform",
            website_url="https://www.netflix.com",
        )
        self.media_stream = models.MediaStream.objects.create(
            title="Avengers Endgame",
            summary="The Avengers must come together and learn to fight as they unravel the mysteries of the super-hero universe",
            platform=self.stream_platform,
            is_active=True,
        )


class StreamPlatformTestCase(BaseTestCase):
    def test_create_stream_platform(self):
        data = {
            "name": "Netflix",
            "about": "Netflix is the largest online streaming platform",
            "website": "https://www.netflix.com",
        }
        response = self.client.post(reverse("stream-platform-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(models.StreamPlatform.objects.count(), 1)
        self.assertEqual(models.StreamPlatform.objects.get().name, "Netflix")

    def test_get_stream_platform_list(self):
        response = self.client.get(reverse("stream-platform-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_stream_platform_detail(self):
        response = self.client.get(
            reverse("stream-platform-detail", args=[self.stream_platform.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_stream_platform(self):
        data = {
            "name": "Netflix Updated",
            "about": "Netflix is the largest online streaming platform",
            "website": "https://www.netflix.com",
        }
        response = self.client.put(
            reverse("stream-platform-detail", args=[self.stream_platform.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_stream_platform(self):
        response = self.client.delete(
            reverse("stream-platform-detail", args=[self.stream_platform.id])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MediaStreamTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_create_media_stream(self):
        data = {
            "title": "Avengers Endgame",
            "summary": "The Avengers must come together and learn to fight as they unravel the mysteries of the super-hero universe",
            "platform": self.stream_platform.id,
            "is_active": True,
        }
        response = self.client.post("/api/cine/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(models.MediaStream.objects.count(), 1)
        self.assertEqual(models.MediaStream.objects.get().title, "Avengers Endgame")

    def test_get_media_stream_list(self):
        response = self.client.get("/api/cine/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_media_stream_detail(self):
        response = self.client.get(reverse("media-detail", args=[self.media_stream.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_media_stream(self):
        data = {
            "title": "Avengers Endgame Updated",
            "summary": "The Avengers must come together and learn to fight as they unravel the mysteries of the super-hero universe",
            "platform": self.stream_platform.id,
            "is_active": True,
        }
        response = self.client.put(
            reverse("media-detail", args=[self.media_stream.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_media_stream(self):
        response = self.client.delete(
            reverse("media-detail", args=[self.media_stream.id])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReviewTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.media_stream2 = models.MediaStream.objects.create(
            title="Dune",
            summary="Dune",
            platform=self.stream_platform,
            is_active=True,
        )
        self.review = models.Review.objects.create(
            reviewer=self.user,
            rating=5,
            media_stream=self.media_stream2,
            description="Wonderful",
            is_active=True,
        )

    def test_create_review(self):
        data = {
            "reviewer": self.user,
            "rating": 5,
            "media-stream": self.media_stream,
            "description": "Great movie",
            "is_active": True,
        }
        response = self.client.post(
            reverse("create-review", args=[self.media_stream.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)

        response = self.client.post(
            reverse("create-review", args=[self.media_stream2.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Review.objects.count(), 2)

    def test_create_review_without_login(self):
        data = {
            "reviewer": self.user,
            "rating": 5,
            "media-stream": self.media_stream,
            "description": "Great movie",
            "is_active": True,
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(
            reverse("create-review", args=[self.media_stream.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_review(self):
        data = {
            "reviewer": self.user,
            "rating": 4,
            "media-stream": self.media_stream,
            "description": "wonderful movie with great acting, animation and music.",
            "is_active": False,
        }
        response = self.client.put(
            reverse("review-detail", args=[self.review.id]), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            models.Review.objects.get().description,
            "wonderful movie with great acting, animation and music.",
        )
        self.assertEqual(models.Review.objects.get().rating, 4)
        self.assertEqual(models.Review.objects.get().is_active, False)

    def test_get_review_list(self):
        response = self.client.get(reverse("review-list", args=[self.media_stream.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_review_detail(self):
        response = self.client.get(reverse("review-detail", args=[self.review.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_review(self):
        response = self.client.delete(reverse("review-detail", args=[self.review.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reviewer(self):
        response = self.client.get(
            "/api/cine/user-reviews/?username=" + self.user.username
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
