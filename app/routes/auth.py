from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import User
from app import db

#  Create a Blueprint for the auth routes
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    """
    Registers A New User.

    Parameters:
    - data (dict): A dictionary containing user registration data.
        - username (str): The username of the new user.
        - email (str): The email address of the new user.
        - password (str): The password of the new user.
        - role (str): The role of the new user.

    Returns:
    - dict: A JSON response indicating the success of the user creation.
        - message (str): A message indicating the success of the user creation.
    """
    # Get the user data from the request
    data = request.get_json()
    # Hash the user's password
    hashed_password = generate_password_hash(data['password'])
    # Create a new user with the provided data
    new_user = User(username=data['username'], email=data['email'], password=hashed_password, role=data['role'])
    # Add the new user to the database
    db.session.add(new_user)
    # Commit the changes to the database 
    db.session.commit()
    # Return a success message
    return jsonify({'message': 'User created successfully'}), 200

@bp.route('/login', methods=['POST'])
def login():
    """
    Authenticates a user and generates an access token.

    Returns:
        A JSON response containing the access token if the user is authenticated, 
        or a JSON response with an error message if the credentials are invalid.
    """
    # Get the user data from the request
    data = request.get_json()
    # Check if the user exists and the password is correct
    user = User.query.filter_by(username=data['username']).first()
    # If the user exists and the password is correct, generate an access token
    if user and check_password_hash(user.password, data['password']):
        # Create an access token for the user
        access_token = create_access_token(identity=user.id)
        #  Return the access token
        return jsonify({'access_token': access_token}), 200
    # If the user does not exist or the password is incorrect, return an error message
    return jsonify({'message': 'Invalid credentials'}), 401
