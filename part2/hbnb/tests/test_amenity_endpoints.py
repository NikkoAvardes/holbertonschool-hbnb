"""Test module for amenity API endpoints."""

import unittest
from app import create_app


class TestAmenityEndpoints(unittest.TestCase):
    """Test cases for amenity-related API endpoints."""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_amenity_invalid_data(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
