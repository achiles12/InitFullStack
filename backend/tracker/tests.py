# backend/tracker/tests.py
# basic API tests

import json
import logging
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

# Configure logging so it prints in test output
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrackerAPITest(APITestCase):
    def setUp(self):
        logger.info("🔧 Setting up test user")
        self.user = User.objects.create_user(username='testuser', password='testpass', role='tenant')
        self.login_url = reverse('token_obtain_pair')
        self.properties_url = '/api/properties/'  # adjust if your route differs
        logger.info(f"✅ Created test user: {self.user.username} ({self.user.role})")

    def test_login(self):
        """Test that login returns valid JWT tokens"""
        logger.info(f"🧪 Testing login at {self.login_url}")
        response = self.client.post(
            self.login_url,
            {'username': 'testuser', 'password': 'testpass'},
            format='json'
        )

        logger.info(f"🔍 Login response: {response.status_code} - {response.content}")

        self.assertEqual(response.status_code, status.HTTP_200_OK, "Login should return 200 OK")
        self.assertIn('access', response.data, "Access token missing in response")
        self.assertIn('refresh', response.data, "Refresh token missing in response")

        self.access_token = response.data['access']
        logger.info("✅ JWT token obtained successfully")

    def test_auth_protected(self):
        """Test that /api/properties/ is protected and requires authentication"""
        logger.info("🧪 Testing unauthorized access to /api/properties/")
        response = self.client.get(self.properties_url)
        logger.info(f"🔍 Unauthorized response: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Now test authorized access
        logger.info("🧪 Testing authorized access after login")
        login_response = self.client.post(
            self.login_url,
            {'username': 'testuser', 'password': 'testpass'},
            format='json'
        )

        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        auth_response = self.client.get(self.properties_url)
        logger.info(f"🔍 Authorized response: {auth_response.status_code}")
        logger.info(f"🔍 Response data: {auth_response.data}")

        # Expecting 200 OK (even if list is empty)
        self.assertEqual(auth_response.status_code, status.HTTP_200_OK)
        logger.info("✅ Protected route accessible with valid JWT token")
