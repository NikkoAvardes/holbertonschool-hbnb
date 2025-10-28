"""Test module for place API endpoints."""

import unittest
from app import create_app


class TestPlaceEndpoints(unittest.TestCase):
    """Test cases for place-related API endpoints."""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        # Créer un utilisateur de test et récupérer son ID
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        user_json = user_resp.get_json()
        self.user_id = (
            user_json["id"] if user_json and "id" in user_json else None
        )

    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_data(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "",
            "price": -10,
            "latitude": 200,
            "longitude": 200
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
