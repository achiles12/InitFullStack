# backend/tracker/tests.py
# basic API tests

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class TrackerAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login(self):
        url = reverse('token_obtain_pair')  # if you have JWT setup # same name added in urls.py
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_auth_protected(self):
        # Example of protected route test
        url = '/api/properties/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

