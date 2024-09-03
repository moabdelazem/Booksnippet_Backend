from app import db
from sqlalchemy import Column, String
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

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), nullable=False)
    password = Column(String(120), nullable=False)
    role = Column(String(20), nullable=False, default="user")


class Book(db.Model):
    """
    Represents a book in the database.

    Attributes:
        id (str): The unique identifier of the book.
        title (str): The title of the book.
        author (str): The author of the book.
        isbn (str): The ISBN number of the book.

    """

    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    title = Column(String(120), nullable=False)
    author = Column(String(80), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
