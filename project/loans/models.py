from project import db,app

class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    loaned_book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    loaned_book = db.relationship('Book', backref=db.backref('loans', lazy=True))
    customer = db.relationship('Customer', backref=db.backref('loans', lazy=True))

    def __init__(self, customer_id, loaned_book_id, loan_date, return_date):
        self.customer_id = customer_id
        self.loaned_book_id = loaned_book_id
        self.loan_date = loan_date
        self.return_date = return_date

def create_loans():
    with app.app_context():
        db.create_all()