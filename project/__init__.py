import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


##########################################
############ DATABASE SETUP ##############
##########################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'library.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

from project.books.models import create_books
from project.customers.models import create_customers
from project.loans.models import create_loans

create_books()
create_customers()
create_loans()

##########################################
######### REGISTER BLUEPRINTS ############
##########################################

from project.books.views import books
from project.customers.views import customers
from project.loans.views import loans

app.register_blueprint(books)
app.register_blueprint(customers)
app.register_blueprint(loans)
