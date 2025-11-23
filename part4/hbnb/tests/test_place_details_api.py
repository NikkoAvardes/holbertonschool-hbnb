import unittest
from app import create_app, db


class PlaceDetailsApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Добавляем тестового пользователя
            from app.models.user import User
            test_user = User(
                first_name='Test',
                last_name='User',
                email='test@example.com',
                password='testpassword'
            )
            db.session.add(test_user)
            db.session.commit()

            # Добавляем тестовый amenity
            from app.models.amenity import Amenity
            test_amenity = Amenity(name='WiFi')
            db.session.add(test_amenity)
            db.session.commit()

            # Добавляем тестовый place
            from app.models.place import Place
            test_place = Place(
                title='Test Place',
                description='Test Description',
                price=100.0,
                latitude=50.0,
                longitude=30.0,
                owner=test_user
            )
            test_place.amenities.append(test_amenity)
            db.session.add(test_place)
            db.session.commit()
            self.test_place_id = test_place.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_place_details_response_fields(self):
        with self.app.app_context():
            response = self.client.get(f'/api/v1/places/{self.test_place_id}')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('title', data)
            self.assertIn('description', data)
            self.assertIn('price', data)
            self.assertIn('owner_id', data)
            self.assertIn('amenities', data)
            self.assertIn('owner', data)

    def test_place_details_amenities_structure(self):
        with self.app.app_context():
            response = self.client.get(f'/api/v1/places/{self.test_place_id}')
            data = response.get_json()
            self.assertIsInstance(data['amenities'], list)
            self.assertGreater(len(data['amenities']), 0)
            for amenity in data['amenities']:
                self.assertIn('id', amenity)
                self.assertIn('name', amenity)


if __name__ == '__main__':
    unittest.main()
