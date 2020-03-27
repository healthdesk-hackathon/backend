from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from project.test_mixins import WithUsersMixin


class AuthTestCase(WithUsersMixin, APITestCase):

    def test_can_get_token(self):
        response = self.client.post(reverse('v1:token_obtain_pair'), {
            'username': 'user',
            'password': 'user_pass'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.json())
        self.assertTrue('refresh' in response.json())

    def test_can_refresh_token(self):
        response = self.client.post(reverse('v1:token_obtain_pair'), {
            'username': 'user',
            'password': 'user_pass'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access_token = response.json()['access']
        refresh_token = response.json()['refresh']

        response = self.client.post(reverse('v1:token_refresh'), {
            'refresh': refresh_token
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.json())
        self.assertFalse(response.json()['access'] == access_token)
