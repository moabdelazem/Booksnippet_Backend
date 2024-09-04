from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import User
from app.database import get_db
from sqlalchemy.orm import Session

# Create the auth blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    Returns:
        A JSON response containing a success message if the user is created successfully,
        or an error message if the username already exists.
    Raises:
        None.
    """
    # Get the request data
    data = request.get_json()
    # Get the database session
    db: Session = next(get_db())
    
    # Check if the username already exists
    existing_user = db.query(User).filter(User.username == data['username']).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    # Hash the password and create a new user
    hashed_password = generate_password_hash(data['password'], method='sha256')
    # Create a new user object
    new_user = User(username=data['username'], password=hashed_password, role=data['role'])
    
    # Add the new user to the database
    db.add(new_user)
    # Commit the transaction
    db.commit()

    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    """
    Logs in a user by checking the provided credentials.
    Returns:
        A JSON response containing an access token if the credentials are valid.
        Otherwise, returns a JSON response with an error message.
    Raises:
        None
    """
    # Get the request data
    data = request.get_json()
    # Get the database session
    db: Session = next(get_db())
    
    # Check if the user exists and the password is correct
    user = db.query(User).filter(User.username == data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        # Create an access token
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    # Return an error message if the credentials are invalid
    return jsonify({'message': 'Invalid credentials'}), 401