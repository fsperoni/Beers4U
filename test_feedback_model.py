"""Message model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Feedback, Like, Dislike

os.environ['DATABASE_URL'] = "postgresql:///beers4u-test"

from app import app

db.create_all()

class FeedbackModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.register("test1", "password", "email1@email.com", "test1", "user1")
        u.id = self.uid
        db.session.add(u)
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_feedback_model(self):
        """Does basic model work?"""
        
        f = Feedback(
            title="feedback title",
            content="this is a feedback",
            recipe_id=1,
            user_id=self.uid
        )

        db.session.add(f)
        db.session.commit()

        # User should have 1 feedback
        self.assertEqual(len(self.u.feedbacks), 1)
        self.assertEqual(self.u.feedbacks[0].title, "feedback title")

    def test_feedback_likes_dislikes(self):
        f1 = Feedback(
            title="a title",
            content="a feedback content",
            recipe_id=1,
            user_id=self.uid
        )

        f2 = Feedback(
            title="another title",
            content="another feedback content",
            recipe_id=2,
            user_id=self.uid 
        )

        u = User.register("test2", "password", "email2@email.com", "test2", "user2")
        uid = 888
        u.id = uid
        db.session.add_all([f1, f2, u])
        db.session.commit()

        u.likes.append(f1)
        u.dislikes.append(f2)

        db.session.commit()

        l = Like.query.filter(Like.user_id == uid).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].feedback_id, f1.id)

        d = Dislike.query.filter(Dislike.user_id == uid).all()
        self.assertEqual(len(d), 1)
        self.assertEqual(d[0].feedback_id, f2.id)
    
    