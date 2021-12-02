"""Models for Feedback app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedbacks = db.relationship('Feedback', cascade='all, delete')

    likes = db.relationship('Feedback', secondary="likes")
    dislikes = db.relationship('Feedback', secondary="dislikes")

    favorites = db.relationship('Favorite', backref="user", cascade='all, delete')

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

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
    
    @classmethod
    def get_fav_rec_ids(cls, id):
        favs = Favorite.query.filter(Favorite.user_id == id).all()
        return [fav.recipe_id for fav in favs]
            

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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    recipe_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', 
        ondelete='cascade'), nullable=False)

    likes = db.relationship('Like', backref="feedback", cascade='all, delete')
    dislikes = db.relationship('Dislike', backref="feedback", cascade='all, delete')

    user = db.relationship('User')

    @property
    def format_date(self):
        """Format date in a more friendly/readable text."""

        return self.created_at.strftime('%b %d %Y at %H:%M') 

class Like(db.Model):
    """Mapping user likes to Feedbacks."""

    __tablename__ = 'likes' 

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    feedback_id = db.Column(db.Integer, db.ForeignKey('feedbacks.id', 
        ondelete='cascade'))

class Dislike(db.Model):
    """Mapping user dislikes to Feedbacks."""

    __tablename__ = 'dislikes' 

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    feedback_id = db.Column(db.Integer, db.ForeignKey('feedbacks.id', 
        ondelete='cascade'))

class Favorite(db.Model):
    """Flagging beer recipe as favorite."""

    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    recipe_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<Favorite #{self.id}: {self.user_id}, {self.recipe_id}>"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)