from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, Blueprint
from project import db
from project.books.models import Book
from project.loans.models import Loan
from flask_cors import  CORS

books = Blueprint('books',__name__,url_prefix='/books')
CORS(books)

# books ->
# get all books
@books.route('/', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_list = [
        {
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'year': book.year,
            'book_type': book.book_type,
            'book_id': book.bk_id,
            'available': book.available
        }
        for book in books
    ]
    return jsonify(books_list), 200

# get specific book with id
@books.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    # Check if a book with the specified book_id exists in the database
    book = Book.query.get(book_id)
    if book is not None:
        return jsonify({'id': book.id, 'name': book.name, 'author': book.author, 'year': book.year, 'book_type': book.book_type, 'book_id': book.bk_id, 'available': book.available} ), 200
    else:
        return jsonify({'error': 'Book with the specific id not found'}), 404

# add book
@books.route('/', methods=['POST'])
def add_book():
    data = request.json
    name = data.get('name')
    author = data.get('author')
    year = data.get('year')
    book_type = data.get('book_type')     
    book_id = data.get('book_id')

    # First validation - if name, author, year, and type haven't been entered
    if not name or not author or not year or book_type not in [1, 2, 3] or not book_id:
        return jsonify({'error': f'Book name, author, year, a valid type (1, 2, or 3), and a valid id are required.'}), 404
    
    # Check if the provided book_id is a 13-digit number
    if book_id and (not book_id.isdigit() or len(book_id) != 13):
        return jsonify({'error': 'Book ID must be a 13-digit number.'}), 404
    
    # Check if the provided book_id already exists in other books
    if book_id and (Book.query.filter_by(bk_id=book_id).first()):
        return jsonify({'error': 'Book with the provided ID already exists.'}), 404
    
    new_book = Book(name=name, author=author, year=year, book_type=book_type, bk_id=book_id)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 200

# update book
@books.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    new_name = data.get('name')
    new_author = data.get('author')
    new_year = data.get('year')
    new_book_type = data.get('book_type')
    new_bk_id = data.get('book_id')
    
    # First validation - if name, author, year, and type haven't been entered
    if not new_name or not new_author or not new_year or new_book_type not in [1, 2, 3]:
        return jsonify({'error': f'Book name, author, year, and a valid type (1, 2, or 3) are required.'}), 404

    # Check if the book with the specified ID exists
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book with the specified ID does not exist'}), 404
    
    # Check if the provided book_id is a 13-digit number
    if new_bk_id and (not new_bk_id.isdigit() or len(new_bk_id) != 13):
        return jsonify({'error': 'Book ID must be a 13-digit number.'}), 400

    # Check if the provided bk_id already exists in other books
    if new_bk_id and Book.query.filter(Book.id != book_id, Book.bk_id == new_bk_id).first():
        return jsonify({'error': 'Book with the provided ID already exists.'}), 400
    
    # Check if a loan with the specified book ID exists
    loan = Loan.query.filter_by(loaned_book_id=book_id).first()
    if loan:
        return jsonify({'error': 'Unable to change book data. Loan of this specified book is currently active'}), 404
    
    # Update book attributes if provided
    if new_name: book.name = new_name
    if new_author: book.author = new_author
    if new_year: book.year = new_year
    if new_book_type: book.book_type = new_book_type
    if new_bk_id: book.bk_id = new_bk_id

    # Commit the changes to the database
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'}), 200

# delete book 
@books.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    # Check if a book with the specified ID exists
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book with the specified ID does not exist'}), 404
    
    # Check if a loan with the specified book ID exists
    loan = Loan.query.filter_by(loaned_book_id=book_id).first()
    if loan:
        return jsonify({'error': 'Loan of this specified book is currently active'}), 404
    
    # Delete the book from the database
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 200

# search book by name
@books.route('/<string:book_name>', methods=['GET'])
def get_book_by_name(book_name):
    # Check if a book with the specified book_id exists in the database
    book = Book.query.filter_by(name=book_name).first()
    if book is not None:
        return jsonify({'id': book.id, 'name': book.name, 'author': book.author, 'year': book.year, 'book_type': book.book_type, 'book_id': book.bk_id, 'available': book.available} ), 200
    else:
        return jsonify({'error': 'Book with the specific name not found'}), 404
