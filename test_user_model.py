"""User model tests."""

import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from models import db, User, Favorite

os.environ['DATABASE_URL'] = "postgresql:///beers4u-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test for user model."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.register("test1", "password", "email1@email.com", "test1", "user1")
        uid1 = 1111
        u1.id = uid1

        u2 = User.register("test2", "password", "email2@email.com", "test2", "user2")
        uid2 = 2222
        u2.id = uid2

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    # User Tests
    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            username="testuser",
            email="test@test.com",
            password="HASHED_PASSWORD",
            first_name="test",
            last_name="user"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.full_name, "test user")
        # User should have no likes, dislikes, nor feedbacks
        self.assertEqual(len(u.likes), 0)
        self.assertEqual(len(u.dislikes), 0)
        self.assertEqual(len(u.feedbacks), 0)


    # Signup Tests 

    def test_valid_register(self):
        u_test = User.register('testtesttest', 'password','testtest@test.com', 'User1', 'Test1')
        uid = 99999
        u_test.id = uid
        db.session.add(u_test)
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtesttest")
        self.assertEqual(u_test.email, "testtest@test.com")
        self.assertNotEqual(u_test.password, "password")
        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))
        self.assertEqual(u_test.first_name, "User1")
        self.assertEqual(u_test.last_name, "Test1")

    def test_invalid_username_register(self):
        invalid = User.register(None, "password","testtest1@test.com", "User1", "Test1")
        uid = 123456789
        invalid.id = uid
        db.session.add(invalid)
        with self.assertRaises(IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_register(self):
        invalid = User.register("test3test", "password", None, "User1", "Test1")
        uid = 123789
        invalid.id = uid
        db.session.add(invalid)
        with self.assertRaises(IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_register(self):
        with self.assertRaises(ValueError) as context:
            User.register("testtest3", "", "email@email.com", "User1", "Test1")
        
        with self.assertRaises(ValueError) as context:
            User.register("test1test", None, "email1@email.com", "User1", "Test1")
    
    def test_invalid_first_name_register(self):
        invalid = User.register("test2test", "password", "email2@email.com", None, "Test1")
        uid = 789
        invalid.id = uid
        db.session.add(invalid)
        with self.assertRaises(IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_last_name_register(self):
        invalid = User.register("testtest4", "password", "email3@email.com", "User1", None)
        uid = 456
        invalid.id = uid
        db.session.add(invalid)
        with self.assertRaises(IntegrityError) as context:
            db.session.commit()

    # Authentication Tests
    
    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.username, self.u1.username)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))

    # Favorite Tests

    def test_favorite_recipe(self):

        u = User.register("test3", "password", "email3@email.com", "test3", "user3")
        uid = 888
        u.id = uid
        fav = Favorite(
            user_id=uid, 
            recipe_id=2
        )
        db.session.add_all([fav, u])
        db.session.commit()

        u.favorites.append(fav)

        db.session.commit()

        f = Favorite.query.filter(Favorite.user_id == uid).all()
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0].user_id, uid)
        self.assertEqual(f[0].recipe_id, 2)