import unittest
import os
import json
from app import create_app, db


class StatusTestCase(unittest.TestCase):
    """This class represents the status test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.status = {'name': 'active'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_business_creation(self):
        """Test API can create a status (POST request)"""
        res = self.client().post('/statuses/', data=self.status)
        self.assertEqual(res.status_code, 201)
        self.assertIn('active', str(res.data))

    def test_api_can_get_all_businesses(self):
        """Test API can get all statuses (GET request)."""
        res = self.client().post('/statuses/', data=self.status)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/statuses/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('active', str(res.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
