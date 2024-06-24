"""
Test for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email successful"""
        # Dummy email and password for test purpose.
        email = 'test@example.com'
        password = 'testpass123'
        # Creation of the user with the dummy email and pw.
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        # Test to check if the user was created successfully
        # By checking the email.
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        # List created for testing purpose of the normalization of emails.
        # 1st element is the email address, 2nd item is the expected
        # normalized email.
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        # Looping sample email and creating a user with each email address
        # and password 'sample123'
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            # Test to check of the normalized email matches the expected
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creates a user without an email raises a valuesErro"""

        # Checking that ValueError message is raised when email is not
        # provided during user creation.
        with self.assertRaises(ValueError):
            # Creating the user w/ out an email.
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Creating a super user"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'sample123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
