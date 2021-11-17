"""Models for Feedback app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """User model"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedbacks = db.relationship('Feedback')

    likes = db.relationship('Feedback', secondary="likes")
    dislikes = db.relationship('Feedback', secondary="dislikes")

    favorites = db.relationship('Favorite', backref="user")

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email,
            first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """
            Validate that user exists & password is correct.
            Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
    
    @property
    def full_name(self):
        """Return the full name of the user"""
        return f"{self.first_name} {self.last_name}"

class Feedback(db.Model):
    """Feedback model"""

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_public = db.Column(db.Boolean, default=False)
    user_name = db.Column(db.String(20), db.ForeignKey('users.username', 
        ondelete='CASCADE'), nullable=False)

    user = db.relationship('User')

class Like(db.Model):
    """Mapping user likes to Feedbacks."""

    __tablename__ = 'likes' 

    id = db.Column( 
        db.Integer,
        primary_key=True
    )

    user_name = db.Column(
        db.String(20),
        db.ForeignKey('users.username', ondelete='cascade')
    )

    feedback_id = db.Column(
        db.Integer,
        db.ForeignKey('feedbacks.id', ondelete='cascade'),
        unique=True
    )

class Dislike(db.Model):
    """Mapping user dislikes to Feedbacks."""

    __tablename__ = 'dislikes' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_name = db.Column(
        db.String(20),
        db.ForeignKey('users.username', ondelete='cascade')
    )

    feedback_id = db.Column(
        db.Integer,
        db.ForeignKey('feedbacks.id', ondelete='cascade'),
        unique=True
    )

class Favorite(db.Model):
    """Flagging beer recipe as favorite."""

    __tablename__ = 'favorites'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_name = db.Column(
        db.String(20),
        db.ForeignKey('users.username', ondelete='cascade')
    )

    recipe_id = db.Column(
        db.Integer
    )


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)