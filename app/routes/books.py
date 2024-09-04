from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import User, Book
from app.database import get_db
from sqlalchemy.orm import Session

# Create the books blueprint
bp = Blueprint('books', __name__, url_prefix='/books')

@bp.route('', methods=['GET'])
@jwt_required()
def get_books():
    """
    Retrieves all books from the database.

    Returns:
        A JSON response containing a list of dictionaries, each representing a book.
        Each dictionary contains the following keys:
            - id: The ID of the book.
            - title: The title of the book.
            - author: The author of the book.
            - isbn: The ISBN of the book.
    """
    # Get the database session
    db: Session = next(get_db())
    # Query all books
    books = db.query(Book).all()
    # Return a JSON response with the list of books
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'isbn': book.isbn} for book in books])

@bp.route('', methods=['POST'])
@jwt_required()
def create_book():
    """
    Creates a new book in the database.
    Returns:
        A JSON response containing a success message and HTTP status code.
    Raises:
        None.
    """
    # Get the database session
    db: Session = next(get_db())
    # Get the current user
    current_user = db.query(User).filter(User.id == get_jwt_identity()).first()
    # Check if the user is an admin
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    # Get the request data
    data = request.get_json()
    # Create a new book object
    new_book = Book(title=data['title'], author=data['author'], isbn=data['isbn'])
    # Add the new book to the database
    db.add(new_book)
    db.commit()
    return jsonify({'message': 'Book added successfully'}), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    """
    Update a book in the database.
    Parameters:
    - id (int): The ID of the book to be updated.
    Returns:
    - dict: A JSON response indicating the status of the update operation.
      - If the update is successful, the response will contain a 'message' key with the value 'Book updated successfully'.
      - If the book is not found, the response will contain a 'message' key with the value 'Book not found'.
      - If the user does not have admin access, the response will contain a 'message' key with the value 'Admin access required'.
    """
    # Get the database session
    db: Session = next(get_db())
    # Get the current user
    current_user = db.query(User).filter(User.id == get_jwt_identity()).first()
    # Check if the user is an admin
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    # Query the book by ID
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    # Get the request data
    data = request.get_json()
    book.title = data['title']
    book.author = data['author']
    book.isbn = data['isbn']
    db.commit()
    return jsonify({'message': 'Book updated successfully'})

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    """
    Delete a book from the database.
    Parameters:
    id (int): The ID of the book to be deleted.
    Returns:
    dict: A dictionary containing the message indicating the result of the deletion.
    Raises:
    None
    """
    # Get DB session
    db: Session = next(get_db())
    # Get the current user
    current_user = db.query(User).filter(User.id == get_jwt_identity()).first()
    # Check if the user is an admin
    if current_user.role != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    
    # Query the book by ID
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    # Delete the book
    db.delete(book)
    db.commit()
    return jsonify({'message': 'Book deleted successfully'})