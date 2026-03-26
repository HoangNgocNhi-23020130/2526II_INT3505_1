from core.database import db

class Book(db.Model):
    __tablename__ = 'books'
    # ID cuốn sách
    id = db.Column(db.Integer, primary_key=True)
    # Mã sách quốc tế
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    # Tiêu đề cuốn sách
    title = db.Column(db.String(200), nullable=False)
    # Tác giả
    author = db.Column(db.String(100), nullable=False)
    # Tổng số lượng
    total_copies = db.Column(db.Integer, default=1)
    # Số sách hiện có (có thể cho mượn)
    available_copies = db.Column(db.Integer, default=1)

    borrow_records = db.relationship('BorrowRecord', backref='book', lazy=True)
    def to_dict(self):
        return {
            "id": self.id,
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies
        }