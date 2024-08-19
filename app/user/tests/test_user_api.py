"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


# URL endpoint to create a user
CREATE_USER_URL = reverse('user:create')
# URL endpoint for creating tokens
TOKEN_URL = reverse('user:token')
# URL end point for retriving user
ME_URL=reverse('user:me')

# Helper function for creating a user
def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

# This class handle the public api request
class PublicUserApiTest(TestCase):
    """Test the public feature of the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""
        # Test user data passed to the API
        payload = {
            'email': 'new@email.com',
            'password': 'Testpass123',
            'name': 'Test Name',
        }
        # Sending post request tp create user
        res = self.client.post(CREATE_USER_URL, payload)
        # Checking if user was created successfully
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Getting the new user's object from data base
        user = get_user_model().objects.get(email = payload['email'])
        # Checking the user's password
        self.assertTrue(user.check_password(payload['password']))
        # Checking that the password is not part of the response.
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        # Creating a user that already exist in the data base
        create_user(**payload)
        # Sending post request to create new user
        res = self.client.post(CREATE_USER_URL, payload)
        # Testing we get bad request since the user we tried adding to
        # the database already exist
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test if an error is returned if password is less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }
        # Seing post request for above user
        res = self.client.post(CREATE_USER_URL, payload)
        # Since the povided password is too short, we expect bad request
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # Checking if the user exits in the data base. Return is a boolean
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        # Verfying that the return is false
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        # User test info
        user_details = {
            'name' : 'Test Name',
            'email' : 'test@example.com',
            'password' : 'test-user-password123',
        }
        # Creating new user
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        # Sending post request for creation of our token
        res = self.client.post(TOKEN_URL, payload)
        # checking if res data has a token
        self.assertIn('token', res.data)
        # Testing if we get 200s
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        # Creaating user
        create_user(email='test@example.com', password='goodpass')
        # Payload
        payload = {'email': 'test@example.com', 'password': 'badpass'}
        # Sending create token request to endpoint
        res = self.client.post(TOKEN_URL, payload)

        # Checking that token was not create
        self.assertNotIn('token', res.data)
        # Checking we get 400 bad request
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {'email': 'test@example.com', 'password': ''}
        # Sending create token request to endpoint
        res = self.client.post(TOKEN_URL, payload)

        # Checking that token was not create
        self.assertNotIn('token', res.data)
        # Checking we get 400 bad request
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthentication(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)
        # Testing we get unauthprized message since we did not authenticated
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# This class handle the private authentication test of the API
class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""
    def setUp(self):
        # Creating test user
        self.user = create_user(
            email='example@email.com',
            password='testpass123',
            name='Test Name',
        )
        # creating client using function from rest framework
        self.client = APIClient()
        # Forcing authentication to specific user
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        # Sending get request
        res = self.client.get(ME_URL)
        # Checking get method returns something successfully
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Checking the returned data matches our user
        self.assertEqual(res.data, {
            'name':self.user.name,
            'email':self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test POST  is not allowed for me endpoint."""
        # Bad post request
        res = self.client.post(ME_URL, {})
        # Checking we can not create with above request
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authentication user."""
        payload = {'name':'Updated Name', 'password' : 'newpassword123'}
        # Seding patch request to modify database values
        res = self.client.patch(ME_URL, payload)
        # Refresh database
        self.user.refresh_from_db()
        # Checking the name matches updated name
        self.assertEqual(self.user.name, payload['name'])
        # Checking new passwpord
        self.assertTrue(self.user.check_password(payload['password']))
        # Checking 200 status code
        self.assertEqual(res.status_code, status.HTTP_200_OK)










