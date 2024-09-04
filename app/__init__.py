from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os
from app.database import engine, Base

# Load the environment variables
load_dotenv()

# Initialize the JWT manager and the database client
jwt = JWTManager()

def create_app():
    """
    Creates and configures the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    # Create the Flask application
    app = Flask(__name__)
    # Set the JWT secret key
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Enable CORS
    CORS(app)
    # Initialize the JWT manager
    jwt.init_app(app)

    # Create the database client
    Base.metadata.create_all(Client.get_engine())

    return app