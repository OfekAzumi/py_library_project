from project import db,app

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100))
    age = db.Column(db.Integer)
    cut_id = db.Column(db.String(9), unique=True, nullable=False)

    def __init__(self, name, city, age, cut_id):
        self.name = name
        self.city = city
        self.age = age
        self.cut_id = cut_id

def create_customers():
    with app.app_context():
        db.create_all()