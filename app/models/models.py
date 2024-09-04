from sqlalchemy import Column, Integer, String
from app.database import Base
import uuid
from sqlalchemy import Column, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="user")

class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)