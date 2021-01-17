from imgRepFlask import create_app
from imgRepFlask.models import User, Account, ContactInfo                      # Using models in views, DB needs to exist first
from flask import request
import unittest

class TestRoutes(unittest.TestCase):

    # Will run before every test
    def setUp(self):
        self.app = create_app()
        self.tester = self.app.test_client(self)

    # Will run after every test
    def tearDown(self):
        del self.app

    # Register Valid User
    def test_register(self):
        user = User()
        response = self.tester.post('/register', data=dict(name='Adam', creator=user, email="test@test.com", password="test"))
        self.assertEqual(response.status_code, 200)

    # Register Invalid User
    def test_register_invalid(self):
        user = User()
        response = self.tester.post('/register', data=dict())
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()