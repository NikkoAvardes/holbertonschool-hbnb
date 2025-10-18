"""Test module for user API endpoints."""

import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):
    """Test cases for user-related API endpoints."""

    def setUp(self):
        """Set up test client before each test."""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        """Test successful user creation with valid data."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        """Test user creation failure with invalid data."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
