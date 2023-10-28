from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, Blueprint
from project import db
from project.customers.models import Customer
from project.loans.models import Loan

customers = Blueprint('customers',__name__,url_prefix='/customers')


# customers ->
# get all customers
@customers.route('/', methods=['GET'])
def get_customers():
    # Query all customers and construct the list of dictionaries
    customers = Customer.query.all()
    customers_list = [
        {
            'id': customer.id,
            'name': customer.name,
            'city': customer.city,
            'age': customer.age,
            'cut_id': customer.cut_id
        }
        for customer in customers
    ]
    return jsonify(customers_list), 200

# get specific customer with id
@customers.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    # Check if a customer with the specified customer_id exists in the database
    customer = Customer.query.get(customer_id)
    if customer is not None:
        return jsonify({
            'id': customer.id,
            'name': customer.name,
            'city': customer.city,
            'age': customer.age,
            'cut_id': customer.cut_id  # Include the new cut_id field
        }), 200
    else:
        return jsonify({'error': 'Customer with the specific id not found'}), 404

# add customer
@customers.route('/', methods=['POST'])
def add_customer():
    data = request.json
    name = data.get('name')
    city = data.get('city')
    age = data.get('age')
    cut_id = data.get('cut_id')  # Get the cut_id from the request

    # First validation - if name, city, and age haven't been entered
    if not name or not city or not age or not cut_id:
        return jsonify({'error': 'Customer name, city, age and id are required.'}), 400

    # Check if the provided cut_id is a 9-digit number
    if cut_id and (not str(cut_id).isdigit() or len(str(cut_id)) != 9):
        return jsonify({'error': 'Customer ID must be a 9-digit number.'}), 400

    # Check if the provided cut_id already exists in other customers
    if cut_id and (Customer.query.filter_by(cut_id=cut_id).first()):
        return jsonify({'error': 'Customer with the provided ID already exists.'}), 400

    new_customer = Customer(name=name, city=city, age=age, cut_id=cut_id)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'}), 200

# update customer
@customers.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.json
    new_name = data.get('name')
    new_city = data.get('city')
    new_age = data.get('age')
    new_cut_id = data.get('cut_id')  # Get the new cut_id from the request

    # First validation - if name, city, and age haven't been entered
    if not new_name or not new_city or not new_age:
        return jsonify({'error': 'Customer name, city, and age are required.'}), 400

    # Check if the customer with the specified ID exists
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer with the specified ID does not exist'}), 404

    # Check if the new cut_id is a 9-digit number
    if new_cut_id and (not str(new_cut_id).isdigit() or len(str(new_cut_id)) != 9):
        return jsonify({'error': 'Customer ID must be a 9-digit number.'}), 400

    # Check if the new cut_id already exists in other customers
    if new_cut_id and Customer.query.filter(Customer.id != customer_id, Customer.cut_id == new_cut_id).first():
        return jsonify({'error': 'Customer with the provided ID already exists.'}), 400

    # Update customer attributes if provided
    if new_name: customer.name = new_name
    if new_city: customer.city = new_city
    if new_age: customer.age = new_age
    if new_cut_id: customer.cut_id = new_cut_id

    # Commit the changes to the database
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'}), 200

# delete customer 
@customers.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    # Check if a customer with the specified ID exists
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer with the specified ID does not exist'}), 404

    # Check if a loan with the specified book ID exists
    loan = Loan.query.filter_by(customer_id=customer_id).first()
    if loan:
        return jsonify({'error': 'Loan of a specified book by this specified customer is currently active'}), 404
    
    # Delete the customer from the database
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200

# search customer by name
@customers.route('/<string:customer_name>', methods=['GET'])
def get_customer_by_name(customer_name):
    customer = Customer.query.filter_by(name = customer_name).first()
    if customer is not None:
        return jsonify({
            'id': customer.id,
            'name': customer.name,
            'city': customer.city,
            'age': customer.age,
            'cut_id': customer.cut_id  # Include the new cut_id field
        }), 200
    else:
        return jsonify({'error': 'Customer with the specific name not found'}), 404
