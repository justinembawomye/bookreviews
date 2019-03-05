import os
import unittest
import json
from application import create_app, db


class UserTestCase(unittest.TestCase):
    """This class represents the user test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.data = {'username': 'Justine', 'email': 'jmbawomye@gmail.com',
            'password': '123456', 'confirm_password': '123456'}
        self.data2 = {'username': '', 'email': 'jmbawomye@gmail.com',
            'password': '123456', 'confirm_password': '123456'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_user_creation(self):
        """Test can create a user (POST request)"""
        res = self.client.post('/register', data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        # self.assertIn('You have successfully created an account! Please login', str(res.data))
    # def test_create_user_who_exits(self):
    #     """Test can create a user (POST request)"""
    #     res = self.client.post('/register', data=json.dumps(self.data), content_type='application/json')
    #     self.assertEqual(res.status_code, 302)

    # def test_create_user_without_credentials(self):
    #     res = self.client.post('/register', data=json.dumps({}), content_type='application/json')
    #     self.assertEqual(res.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()    
