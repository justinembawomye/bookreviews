import os
import unittest
import json
from application import create_app, db

class UserTestCase(unittest.TestCase):
    """This class represents the user test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.username = {'username': 'Go for vacation'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_creation(self):
        """Test can create a user (POST request)"""
        res = self.client().post('/register', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Go for vacation', str(res.data))



    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()    