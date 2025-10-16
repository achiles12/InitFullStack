# backend/tracker/tests.py
# basic API tests

import logging
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from tracker.models import Property, MaintenanceIssue, RepairJob, Message

User = get_user_model()

# Configure logging for clear console output
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrackerAPITest(APITestCase):
    """Integration test suite for all core API endpoints"""

    def setUp(self):
        logger.info("🔧 Setting up test data...")
        self.user = User.objects.create_user(username='tenantuser', password='tenantpass', role='tenant')
        self.landlord = User.objects.create_user(username='landlord', password='landpass', role='landlord')
        self.handyman = User.objects.create_user(username='handyman', password='handpass', role='handyman')

        # URLs
        self.login_url = reverse('token_obtain_pair')
        self.property_url = '/api/properties/'
        self.issue_url = '/api/issues/'
        self.job_url = '/api/jobs/'
        self.message_url = '/api/messages/'

        logger.info(f"✅ Created test users: {self.user.username}, {self.landlord.username}, {self.handyman.username}")

    def authenticate(self, username='tenantuser', password='tenantpass'):
        """Helper to get JWT and set header"""
        logger.info(f"🔐 Logging in as {username}")
        res = self.client.post(self.login_url, {'username': username, 'password': password}, format='json')
        logger.info(f"🔍 Login response {res.status_code}: {res.data}")
        self.assertEqual(res.status_code, status.HTTP_200_OK, f"Login failed for {username}")
        token = res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        logger.info(f"✅ Authenticated with JWT for {username}")

    def test_login_and_auth(self):
        """✅ Test basic login + auth protection"""
        logger.info("🧪 Testing login + auth protection flow...")
        self.authenticate()
        response = self.client.get(self.property_url)
        logger.info(f"🔍 Authenticated access response: {response.status_code}")
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])

    def test_property_crud(self):
        """🏠 Test Property creation, retrieval, update, deletion"""
        self.authenticate('landlord', 'landpass')

        # Create
        logger.info("🧪 Creating property...")
        prop_data = {'name': 'Test Apartment', 'address': '123 Street', 'description': 'Nice place'}
        res = self.client.post(self.property_url, prop_data, format='json')
        logger.info(f"🔍 Create response: {res.status_code} - {res.data}")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        prop_id = res.data['id']

        # List
        res = self.client.get(self.property_url)
        logger.info(f"🔍 List properties: {res.data}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Update
        update_data = {'description': 'Updated desc'}
        res = self.client.patch(f"{self.property_url}{prop_id}/", update_data, format='json')
        logger.info(f"🔍 Update response: {res.status_code} - {res.data}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Delete
        res = self.client.delete(f"{self.property_url}{prop_id}/")
        logger.info(f"🔍 Delete response: {res.status_code}")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        logger.info("✅ Property CRUD test passed")

    def test_issue_crud(self):
        """🛠️ Test Maintenance Issue creation and update"""
        self.authenticate('tenantuser', 'tenantpass')
        landlord_property = Property.objects.create(
            landlord=self.landlord, name='Condo', address='Makati', description='High-rise unit'
        )

        logger.info("🧪 Creating maintenance issue...")
        issue_data = {
            'property': landlord_property.id,
            'title': 'Leaky faucet',
            'description': 'The kitchen sink is dripping',
        }
        res = self.client.post(self.issue_url, issue_data, format='json')
        logger.info(f"🔍 Create issue response: {res.status_code} - {res.data}")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        issue_id = res.data['id']

        # Update status
        self.authenticate('landlord', 'landpass')
        res = self.client.patch(f"{self.issue_url}{issue_id}/", {'status': 'in_progress'}, format='json')
        logger.info(f"🔍 Update issue: {res.status_code} - {res.data}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        logger.info("✅ Issue CRUD test passed")

    def test_job_creation_and_completion(self):
        """🔧 Test RepairJob creation by landlord and update by handyman"""
        prop = Property.objects.create(landlord=self.landlord, name='Condo', address='Taguig')
        issue = MaintenanceIssue.objects.create(
            property=prop, reported_by=self.user, title='Broken window', description='Needs fixing'
        )

        self.authenticate('landlord', 'landpass')
        job_data = {'issue': issue.id, 'handyman': self.handyman.id, 'notes': 'Please fix ASAP'}
        res = self.client.post(self.job_url, job_data, format='json')
        logger.info(f"🔍 Create job: {res.status_code} - {res.data}")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        job_id = res.data['id']

        # Handyman updates completion
        self.authenticate('handyman', 'handpass')
        res = self.client.patch(f"{self.job_url}{job_id}/", {'notes': 'Fixed window', 'cost': '200.00'}, format='json')
        logger.info(f"🔍 Handyman update: {res.status_code} - {res.data}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        logger.info("✅ RepairJob test passed")

    def test_message_flow(self):
        """💬 Test sending and listing messages"""
        prop = Property.objects.create(landlord=self.landlord, name='Condo', address='Taguig')
        issue = MaintenanceIssue.objects.create(
            property=prop, reported_by=self.user, title='Leaky roof', description='Water dripping'
        )

        self.authenticate('tenantuser', 'tenantpass')
        msg_data = {'issue': issue.id, 'content': 'Please fix soon!'}
        res = self.client.post(self.message_url, msg_data, format='json')
        logger.info(f"🔍 Create message: {res.status_code} - {res.data}")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # List messages
        res = self.client.get(f"{self.message_url}?issue={issue.id}")
        logger.info(f"🔍 List messages: {res.status_code} - {res.data}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        logger.info("✅ Message flow test passed")
