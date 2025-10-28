"""Test module for review API endpoints."""

import unittest
from app import create_app


class TestReviewEndpoints(unittest.TestCase):
    """Test cases for review-related API endpoints."""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review(self):
        # Créer un utilisateur
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com"
        })
        user_id = user_resp.get_json()["id"]

        # Créer une place
        place_resp = self.client.post('/api/v1/places/', json={
            "title": "Nice House",
            "description": "A beautiful house",
            "price": 150.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": user_id
        })
        place_id = place_resp.get_json()["id"]

        # Créer un review avec les vrais IDs
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_data(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 6,  # Invalid rating (should be 1-5)
            "user_id": "",
            "place_id": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
