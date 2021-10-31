"""Tests for user authentication."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserAuthTest(TestCase):
    """Test for authenticated user."""

    def setUp(self):
        """Initialize the user for test."""
        # superclass setUp creates a Client object and initializes database
        super().setUp()
        self.user = {
            "username": "testuser",
            "password": "FatChance!",
            "email": "testuser@nowhere.com"
        }
        self.user1 = User.objects.create_user(**self.user)
        self.user1.first_name = "Tester"
        self.user1.save()

    def test_login_view(self):
        """Test that a user can login via the login view."""
        login_url = reverse("login")
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        response = self.client.post(login_url, self.user)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("polls:index"))

    def test_logout_view(self):
        """Test that user can log out via the logout view."""
        self.client.post(reverse('login'), self.user)
        logout_url = reverse("logout")
        response = self.client.post(logout_url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("polls:index"))
