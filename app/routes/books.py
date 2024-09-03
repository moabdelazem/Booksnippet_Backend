from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import User, Book
from app import db

bp = Blueprint("books", __name__, url_prefix="/books")


# Get All Books In The Library
@bp.route("", methods=["GET"])
@jwt_required()
def get_books():
    """
    Get all books from the database.

    Returns:
        A JSON response containing all books in the database.
    """
    # Query all books from the database
    books = Book.query.all()
    # Serialize the books
    books_data = [
        {"id": book.id, "title": book.title, "author": book.author, "isbn": book.isbn}
        for book in books
    ]
    # Return the serialized books
    return jsonify(books_data), 200


# Create A New Book
@bp.route("", methods=["POST"])
@jwt_required()
def add_book():
    """
    Adds a new book to the database.
    Returns:
        A JSON response indicating the success of the operation.
    """
    # Check if the current user is an admin
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != "admin":
        return jsonify({"message": "Admin access required"}), 403

    # Get the book data from the request
    data = request.get_json()
    # Create a new book with the provided data
    new_book = Book(title=data["title"], author=data["author"], isbn=data["isbn"])
    # Add the new book to the database
    db.session.add(new_book)
    # Commit the changes to the database
    db.session.commit()
    return jsonify({"message": "Book added successfully"}), 201


# Update A Book
@bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_book(id):
    """
    Update a book.
    Parameters:
    - book_id (str): The ID of the book to be updated.
    Returns:
    - dict: A dictionary containing the message indicating the result of the update.
    Raises:
    - 403 Forbidden: If the current user is not an admin.
    - 404 Not Found: If the book with the given ID is not found.
    """
    # Check if the current user is an admin
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != "admin":
        return jsonify({"message": "Admin access required"}), 403

    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    data = request.get_json()
    book.title = data["title"]
    book.author = data["author"]
    book.isbn = data["isbn"]
    db.session.commit()
    return jsonify({"message": "Book updated successfully"})


@bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_book(id):
    """
    Delete a book by its ID.
    Parameters:
    - id (int): The ID of the book to be deleted.
    Returns:
    - dict: A dictionary containing a message indicating the result of the deletion.
    Raises:
    - 403: If the current user is not an admin.
    - 404: If the book with the given ID is not found.
    """
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != "admin":
        return jsonify({"message": "Admin access required"}), 403

    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"})
