from imgRepFlask import create_app, db
from imgRepFlask.models import User, Account, ContactInfo                      # Using models in views, DB needs to exist first
import unittest

class TestRoutes(unittest.TestCase):

    # Will run before every test
    def setUp(self):
        self.app = create_app()
        self.tester = self.app.test_client(self)

    # Will run after every test
    def tearDown(self):
        del self.app
        db.session.remove()

    # Access external page logged out
    def test_user_save(self):
        user = User()

        db.session.add(user)

        account = Account(email="test@test.com", password="password", creator=user)
        contactInfo = ContactInfo(name="tester", creator=user)

        db.session.add(contactInfo)
        db.session.add(account)

        db.commit()

        assert user in db.sesion

if __name__ == '__main__':
    unittest.main()