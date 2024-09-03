from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import os

# Load the environment variables
load_dotenv()

# Setting up the database and JWT
db = SQLAlchemy()
jwt = JWTManager()


def create_superuser():
    """Create a superuser with admin access if not already present."""
    from app.models.models import User  # Import User model

    try:
        superuser = User.query.filter_by(username="admin").first()
        if superuser is None:
            hashed_password = generate_password_hash("admin_password", method="scrypt")
            superuser = User(
                id="19aeb2c7-9ad7-4bfd-9fa3-3982931b50f3",
                username="admin",
                email="mabdelazemahmed@gmail.com",
                password=hashed_password,
                role="admin",
            )
            db.session.add(superuser)
            db.session.commit()
            print("Superuser created successfully")
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error creating superuser: {e}")


# Create the Flask app
def create_app() -> Flask:
    """
    Creates and configures the Flask application.

    Returns:
        Flask: The configured Flask application.
    """

    # Get The Secret Data From Environment Variables
    URI = os.getenv("TURSO_DATABASE_URI")
    AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    dbUrl = f"sqlite:///{URI}"

    # Create the Flask app
    app = Flask(__name__)
    # Configure the app
    app.config["SQLALCHEMY_DATABASE_URI"] = dbUrl
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

    # Set the Turso-specific headers for authentication (if needed)
    # if AUTH_TOKEN:
    #     app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    #         "connect_args": {"headers": {"Authorization": f"Bearer {AUTH_TOKEN}"}}
    #     }

    engine = create_engine(
        dbUrl, connect_args={"headers": {"Authorization": f"Bearer {AUTH_TOKEN}"}}
    )

    # Enable CORS
    CORS(app)
    # Initialize the database and JWT
    db.init_app(app)
    jwt.init_app(app)

    from .routes import auth, books

    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)

    # Create the database tables
    with app.app_context():
        db.create_all()  # Create the database tables
        create_superuser()  # Create the superuser on app initialization

    return app
