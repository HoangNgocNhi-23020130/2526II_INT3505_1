from core.database import db
from datetime import date

class Reader(db.Model):
    __tablename__ = 'readers'

    # ID độc giả
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Họ và tên
    name = db.Column(db.String(100), nullable=False)
    # email
    email = db.Column(db.String(150), unique=True, nullable=False)
    # Sđt liên hệ
    phone = db.Column(db.String(20))
    # Ngày đăng kí
    membership_date = db.Column(db.Date, default=date.today)

    borrow_records = db.relationship('BorrowRecord', backref='reader', lazy=True)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            # Chuyển đổi object ngày tháng thành chuỗi ISO format (YYYY-MM-DD) để JSON có thể đọc được
            "membership_date": self.membership_date.isoformat() if self.membership_date else None
        }