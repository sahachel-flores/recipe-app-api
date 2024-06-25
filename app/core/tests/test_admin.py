"""
Tests for the django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTest(TestCase):
    """Tests for Django admin."""

    # Set up for creating 2 users
    def setUp(self):
        """Create user and client."""
        # Creating superuser.
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        # Login as superuser.
        self.client.force_login(self.admin_user)
        # Creating normal user.
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_lists(self):
        """Test that users are listed on page."""
        # Get url which shows the list of users. Read django
        # documentation to learn how reverse works
        # URL for the changelist
        url = reverse('admin:core_user_changelist')
        # Response object from above url
        res = self.client.get(url)

        # Check response contains username and email
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        # URL for the change user page
        url = reverse('admin:core_user_change', args=[self.user.id])
        # Get URL
        res = self.client.get(url)
        # Check if URL is load successfully
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        # Since we are creating a user, we dont need
        # to pass an argument.
        url = reverse('admin:core_user_add')
        # Get URL
        res = self.client.get(url)
        # Check for 200 code (successful creation)
        self.assertEqual(res.status_code, 200)
