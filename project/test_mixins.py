from django.urls import reverse
from rest_framework.test import APITestCase

from custom_auth.utils import setup_auth_test_data


class WithUsersMixin(APITestCase):

    @classmethod
    def setUpUserData(cls):
        setup_auth_test_data()

    @classmethod
    def setUpTestData(cls):
        cls.setUpUserData()

    def as_user(self):
        self.client.logout()
        self.client.credentials()

        response = self.client.post(reverse('v1:token_obtain_pair'), {
            'username': 'user',
            'password': 'user_pass'
        })

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json()['access'])
        return self.client

    def as_admin(self):
        self.client.logout()
        self.client.credentials()

        response = self.client.post(reverse('v1:token_obtain_pair'), {
            'username': 'admin',
            'password': 'admin_pass'
        })

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json()['access'])
        return self.client
