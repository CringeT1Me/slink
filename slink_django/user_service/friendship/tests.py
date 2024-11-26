from django.core import mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from friendship.models import PENDING, ACCEPTED

User = get_user_model()


def generate_user1_info():

    return {
        "first_name": "testfirstname",
        "last_name": "testlastname",
        'email': 'testemail1@gmail.com',
        "username": "testusername1",
        "password": "strongpassword123",
    }

def generate_user2_info():

    return {
        "first_name": "testfirstname",
        "last_name": "testlastname",
        'email': 'testemail2@gmail.com',
        "username": "testusername2",
        "password": "strongpassword123",
    }

class FriendshipViewSetTest(APITestCase):
    def setUp(self):
        self.user1_info = generate_user1_info()
        self.user2_info = generate_user2_info()
        url = reverse("user-list")
        response = self.client.post(url, self.user1_info)
        self.user1 = User.objects.get(id=response.data['id'])
        response = self.client.post(url, self.user2_info)
        self.user2 = User.objects.get(id=response.data['id'])

        self.activate_user()
        self.create_friend_request()

    def activate_user(self):
        """Проверка активации аккаунта"""
        self.assertEqual(len(mail.outbox), 2)
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

        email_body = mail.outbox[1].body
        activation_url = [line for line in email_body.split() if '/activation/' in line][0]
        activation_url_uid = activation_url.split('/')[-2]
        activation_url_token = activation_url.split('/')[-1]

        activation_backend_url = reverse('user-activation')
        activation_response = self.client.post(
            activation_backend_url,
            {'uid': activation_url_uid, 'token': activation_url_token}
        )
        self.assertEqual(activation_response.status_code, 204)

    def create_friend_request(self):
        url = reverse("jwt-create")
        user1_data = {
            "username": self.user1_info['username'],
            "password": self.user1_info['password'],
        }



        response = self.client.post(url, user1_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user1_access_token = response.data['access']



        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user1_access_token}")

        url = reverse('friendship-list')
        user2 = self.user2
        data = {
            'to_user': user2.id
        }
        friend_request = self.client.post(url, data)
        self.assertEqual(friend_request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(friend_request.data['status'], PENDING)

    def test_cancel_friend_request(self):
        """
        Отмена заявки в друзья отправителем.
        """
        url = reverse("jwt-create")
        user1_data = {
            "username": self.user1_info['username'],
            "password": self.user1_info['password'],
        }
        response = self.client.post(url, user1_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user1_access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user1_access_token}")

        url = '/api/v1/friendship/'
        user2 = self.user2
        data = {
            'to_user': user2.id
        }
        friend_request = self.client.delete(url, data)
        self.assertEqual(friend_request.status_code, status.HTTP_200_OK)

    def test_accept_friend_request(self):
        """
        Принятие запроса в друзья.
        """
        url = reverse("jwt-create")
        user2_data = {
            "username": self.user2_info['username'],
            "password": self.user2_info['password'],
        }
        response = self.client.post(url, user2_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user2_access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user2_access_token}")

        url = '/api/v1/friendship/accept/'
        user1 = self.user1
        data = {
            'to_user': user1.id
        }
        friend_request = self.client.post(url, data)
        self.assertEqual(friend_request.status_code, status.HTTP_200_OK)
        self.assertEqual(friend_request.data['status'], ACCEPTED)

    def test_get_user1_friend_list(self):
        """
        Просмотр списка друзей первого пользователя.
        """
        self.test_accept_friend_request()
        url = reverse("jwt-create")
        user1_data = {
            "username": self.user1_info['username'],
            "password": self.user1_info['password'],
        }
        response = self.client.post(url, user1_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user1_access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user1_access_token}")

        url = f'/api/v1/users/{self.user1_info['username']}/friends/'
        friend_request = self.client.get(url)
        self.assertEqual(friend_request.status_code, status.HTTP_200_OK)

        expected_data = [{
            'id': self.user2.id,
            'username': 'testusername2',
            'first_name': 'Testfirstname',
            'last_name': 'Testlastname',
            'email': 'testemail2@gmail.com',
            'phone': None,
            'description': None,
            'is_active': True,
            'city': None,
            'city_name': None,
            'country': None,
            'country_name': None,
            'avatar_url': None
        }]

        self.assertEqual(friend_request.data, expected_data)

    def test_get_user2_friend_list(self):
        """
        Просмотр списка друзей второго пользователя.
        """
        self.test_accept_friend_request()
        url = reverse("jwt-create")
        user2_data = {
            "username": self.user2_info['username'],
            "password": self.user2_info['password'],
        }
        response = self.client.post(url, user2_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user2_access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user2_access_token}")

        url = f'/api/v1/users/{self.user2_info['username']}/friends/'
        friend_request = self.client.get(url)
        self.assertEqual(friend_request.status_code, status.HTTP_200_OK)

        expected_data = [{
            'id': self.user1.id,
            'username': 'testusername1',
            'first_name': 'Testfirstname',
            'last_name': 'Testlastname',
            'email': 'testemail1@gmail.com',
            'phone': None,
            'description': None,
            'is_active': True,
            'city': None,
            'city_name': None,
            'country': None,
            'country_name': None,
            'avatar_url': None
        }]

        self.assertEqual(friend_request.data, expected_data)



    def test_decline_friend_request(self):
        """
        Отклонение заявки в друзья.
        """
        url = reverse("jwt-create")
        user2_data = {
            "username": self.user2_info['username'],
            "password": self.user2_info['password'],
        }
        response = self.client.post(url, user2_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user2_access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {user2_access_token}")


        url = '/api/v1/friendship/decline/'
        user1 = self.user1
        data = {
            'to_user': user1.id
        }
        friend_request = self.client.delete(url, data)
        self.assertEqual(friend_request.status_code, status.HTTP_200_OK)



