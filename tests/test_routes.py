from imgRepFlask import create_app
import unittest

class TestRoutes(unittest.TestCase):

    # Will run before every test
    def setUp(self):
        self.app = create_app()
        self.tester = self.app.test_client(self)

    # Will run after every test
    def tearDown(self):
        del self.app

    # Access external page logged out
    def test_login_route(self):
        response = self.tester.get('/login', content_type='/html/text')
        self.assertEqual(response.status_code, 200)

    # Access external page logged out
    def test_register_route(self):
        response = self.tester.get('/register', content_type='/html/text')
        self.assertEqual(response.status_code, 200)

    # Access internal page logged out
    def test_account_update(self):
        response = self.tester.get('/account/updateInfo', content_type='/html/text')
        self.assertEqual(response.status_code, 302)

    # Access internal page logged out
    def test_account_update(self):
        response = self.tester.get('/account/updateInfo', content_type='/html/text')
        self.assertEqual(response.status_code, 302)

    # Access page that doesnt exist
    def test_account_reset_password(self):
        response = self.tester.get('/test', content_type='/html/text')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()