from project import db,app

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    book_type = db.Column(db.Integer, nullable=False) # 1 - up to 10, 2 - up to 5, 3 - up to 2
    available = db.Column(db.Boolean, nullable=False)
    bk_id = db.Column(db.String(13), unique=True, nullable=False)

    def __init__(self, name, author, year, book_type, bk_id, available = True):
        self.name = name
        self.author = author
        self.year = year
        self.book_type = book_type
        self.bk_id = bk_id
        self.available = available

def create_books():
    with app.app_context():
        db.create_all()
