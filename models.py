"""SQLAlchemy models for ShareBnB."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import jwt

load_dotenv()

secret_key= os.environ['SECRET_KEY']
bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
    )

    last_name = db.Column(
        db.Text,
        nullable=False
    )

    # image_url = db.Column(
    #     db.Text,
    #     default=DEFAULT_IMAGE_URL,
    # )

    bio = db.Column(
        db.Text,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    is_host = db.Column(
        db.Boolean,
        nullable=False,
    )

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )
        token = User.token(username)

        db.session.add(user)
        return [user, token]

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                token = User.token(username)
                return [user, token]

        return False
    
    @classmethod
    def create_token(cls, username):
        """Create token for user"""
        token = jwt({'username': username }, secret_key)
        return token
    
    def serialize(self):
        """Serialize to dictionary."""

        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "bio": self.bio,
            "is_host": self.is_host
        }



class Listing(db.Model):
    """An individual property listings."""

    __tablename__ = 'listings'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.String(20),
        nullable=False,
    )

    location = db.Column(
        db.String(20),
        nullable=False,
    )

    description = db.Column(
        db.String(500),
        nullable=False,
    )

    price = db.Column(
        db.Integer,
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    rating = db.Column(
        db.Integer,
        nullable=False,
    )

    def serialize(self):
        """Serialize to dictionary."""

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "image_url": self.image_url,
            "user_id": self.user_id,
            "rating": self.rating,
        }


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
