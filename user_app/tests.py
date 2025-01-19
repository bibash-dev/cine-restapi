from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


client = APIClient()


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
            "username": "bibash",
            "email": "bibash@cine.com",
            "password": "bibash123",
            "confirm_password": "bibash123",
        }
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "bibash")
        self.assertEqual(User.objects.get().email, "bibash@cine.com")


class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="bibash", email="bibash@cine.com", password="bibash123"
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access = str(self.refresh.access_token)

    def test_login(self):
        data = {"username": "bibash", "password": "bibash123"}
        response = self.client.post(reverse("token_obtain_pair"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data.keys())
        self.assertIn("refresh", response.data.keys())

    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.user.delete()
