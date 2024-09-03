from app import db
import uuid

class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (str): The unique identifier of the user.
        username (str): The username of the user.
        password (str): The password of the user.
        role (str): The role of the user.
    """
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

class Book(db.Model):
    """
    Represents a book in the database.

    Attributes:
        id (str): The unique identifier of the book.
        title (str): The title of the book.
        author (str): The author of the book.
        isbn (str): The ISBN number of the book.

    """
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)