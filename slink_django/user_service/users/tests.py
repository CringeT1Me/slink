from django.core import mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


def generate_user_info():

    return {
        "first_name": "testfirstname",
        "last_name": "testlastname",
        'email': 'testemail@gmail.com',
        "username": "testusername",
        "password": "strongpassword123",
    }

class UserViewSetTest(APITestCase):
    def setUp(self):
        self.user_info = generate_user_info()
        url = reverse("user-list")
        response = self.client.post(url, self.user_info)
        self.user = User.objects.get(id=response.data['id'])

        self.activate_user()

    def activate_user(self):
        """Проверка активации аккаунта"""
        self.assertEqual(len(mail.outbox), 1)
        email_body = mail.outbox[0].body

        activation_url = [line for line in email_body.split() if '/activation/' in line][0]
        activation_url_uid = activation_url.split('/')[-2]
        activation_url_token = activation_url.split('/')[-1]

        activation_backend_url = reverse('user-activation')
        activation_response = self.client.post(
            activation_backend_url,
            {'uid': activation_url_uid, 'token': activation_url_token}
        )
        self.assertEqual(activation_response.status_code, 204)

    def test_create_user(self):
        """Проверка на получение данных о пользователе."""
        user = self.user
        url = reverse("jwt-create")
        data = {
            "username": self.user_info["username"],
            "password": self.user_info["password"],
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        url = f'/api/v1/users/{user.username}/'
        get_user = self.client.get(url)
        self.assertEqual(get_user.status_code, status.HTTP_200_OK)
        self.assertEqual(get_user.data["id"], user.id)
        self.assertEqual(get_user.data["email"], user.email)

    def test_token(self):
        """Проверка генерации токена."""
        user = self.user
        url = reverse("jwt-create")
        data = {
            "username": user.username,
            "password": self.user_info["password"],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("access"))
        self.assertIsNotNone(response.data.get("refresh"))
