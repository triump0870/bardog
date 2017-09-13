import unittest
import os
import json
from app import create_app, db
from app.models import Status, Vendor


class BusinessTestCase(unittest.TestCase):
    """This class represents the business test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.vendor = {
            'name': 'xyz'
        }
        self.business = {
            'name': 'abc',
            'status': 'active'
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_business_creation(self):
        """Test API can create a business (POST request)"""
        res = self.client().post('/businesses/', data=self.business)
        self.assertEqual(res.status_code, 201)
        self.assertIn('abc', str(res.data))

    def test_api_can_get_all_businesses(self):
        """Test API can get all businesses (GET request)."""
        res = self.client().post('/businesses/', data=self.business)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/businesses/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('abc', str(res.data))

    def test_partnarship(self):
        res = self.client().post('/businesses/', data=self.business)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/vendors/', data=self.vendor)
        self.assertEqual(res.status_code, 201)
        data = {
            'name': 'abc',
            'vendor': 'xyz'
        }
        res = self.client().patch('/businesses/', data=data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('xyz', str(res.data['vendors']))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
