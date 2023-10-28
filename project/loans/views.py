import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, Blueprint
from project import db
from project.loans.models import Loan
from project.customers.models import Customer
from project.books.models import Book

loans = Blueprint('loans',__name__,url_prefix='/loans')

# loans ->
# get loans
@loans.route('/', methods=['GET'])
def get_loans():
    # Query the database to get all loans with customer, book, and book name information
    loans_data = Loan.query.join(Customer).join(Book).add_columns(
        Loan.id, Loan.customer_id, Loan.loaned_book_id, Customer.name.label('customer_name'), Book.name.label('book_name'), Loan.loan_date, Loan.return_date
    ).all()
    # Create a list of dictionaries with loan information
    loans_list = [
        {
            'id': loan.id,
            'c_id': loan.customer_id,
            'b_id': loan.loaned_book_id,
            'customer': loan.customer_name,  # Use the alias 'customer_name' for the customer's name
            'book': loan.book_name,  # Use the alias 'book_name' for the book's name
            'loan_date': loan.loan_date.strftime('%Y-%m-%d'),
            'return_date': loan.return_date.strftime('%Y-%m-%d')
        }
        for loan in loans_data
    ]
    return jsonify(loans_list), 200

# get a specific loan with id
@loans.route('/<int:loan_id>', methods=['GET'])
def get_loan(loan_id):
    # Check if a loan with the specified loan_id exists in the database
    loan = Loan.query.get(loan_id)
    if loan is not None:
        return jsonify({
            'id': loan.id,
            'c_id': loan.customer_id,
            'b_id': loan.loaned_book_id,
            'customer': loan.customer.name,
            'book': loan.loaned_book.name,
            'loan_date': loan.loan_date.strftime('%Y-%m-%d'),
            'return_date': loan.return_date.strftime('%Y-%m-%d')
        }), 200
    else:
        return jsonify({'error': 'Loan with the specific id not found'}), 404

# get late loans
@loans.route('/late', methods=['GET'])
def get_late_loans():
    # Query the database to get all loans with customer, book, and book name information
    loans_data = Loan.query.join(Customer).join(Book).add_columns(
        Loan.id, Loan.customer_id, Loan.loaned_book_id, Customer.name.label('customer_name'), Book.name.label('book_name'), Loan.loan_date, Loan.return_date
    ).all()
    # Create a list of dictionaries with loan information
    loans_list=[]
    for loan in loans_data:
        if (loan.return_date < datetime.date.today()):
            loans_list.append(
                {
                    'id': loan.id,
                    'c_id': loan.customer_id,
                    'b_id': loan.loaned_book_id,
                    'customer': loan.customer_name,  # Use the alias 'customer_name' for the customer's name
                    'book': loan.book_name,  # Use the alias 'book_name' for the book's name
                    'loan_date': loan.loan_date.strftime('%Y-%m-%d'),
                    'return_date': loan.return_date.strftime('%Y-%m-%d')
                })
    if loans_list: return jsonify(loans_list), 200
    else: return jsonify({'error': 'No late loans'}), 400

# add loan
@loans.route('/', methods=['POST'])
def add_loan():
    data = request.json
    c_id = data.get('c_id')
    b_id = data.get('b_id')
    
    # First validation - if b_id and c_id hasn't been entered
    if not c_id or not b_id:
        return jsonify({'error': 'Customer ID and Book ID are are required'}), 400
    
    # Check if a customer with the specified c_id exists in the database
    customer = Customer.query.get(c_id)
    if customer is None:
        return jsonify({'error': 'Customer with the specific id not found'}), 404
    # Check if a book with the specified b_id exists in the database
    book = Book.query.get(b_id)
    if book is None:
        return jsonify({'error': 'Book with the specific id not found'}), 404
    # Check if the book is available for loan
    if book.available == False:
        return jsonify({'error': 'The book has already been loaned'}), 400
    
    ldate = datetime.date.today()
    rdate = ldate
    # Check what type, and change return_date according to type.
    if book.book_type == 1: rdate = ldate + datetime.timedelta(days=10)
    elif book.book_type == 2: rdate = ldate + datetime.timedelta(days=5)
    elif book.book_type == 3: rdate = ldate + datetime.timedelta(days=2)
    else: jsonify({'error': f'The book {book.name} is missing a type. Update book_type'}), 404

    loan = Loan(customer_id=c_id, loaned_book_id=b_id, loan_date=ldate, return_date=rdate)
    db.session.add(loan)
    book.available = False
    db.session.commit()
    return jsonify({'message': f'Loan added successfully. {book.name} has been loaned by {customer.name} from {ldate} up to {rdate}'}), 201

# delete loan 
@loans.route('/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    # Check if there is an active loan with the specified book_id
    loan = Loan.query.get(loan_id)
    if loan:
        late = False
        if (loan.return_date < datetime.date.today()):
            late = True
            delay = datetime.date.today() - loan.return_date
        loaned_book = Book.query.get(loan.loaned_book_id)
        loaned_book.available = True
        db.session.delete(loan)
        db.session.commit()
        if late: return jsonify({'message': f'Loan is closed, but, you are late by {delay.days} days.'}), 400
        else: return jsonify({'message': f'Loan closed successfully. {loaned_book.name} is available again.'}), 200
    else:
        return jsonify({'error': 'No active loan with this ID'}), 404
