from flask import Blueprint, request, jsonify
from models.books import Book
from core.database import db
from models.borrow_records import BorrowRecord
from datetime import datetime, timedelta

# Tạo một Blueprint cho books
book_bp = Blueprint('books', __name__)

# Hàm chuẩn hóa Response
def send_response(success=True, data=None, message="", status_code=200):
    return jsonify({
        "success": success,
        "message": message,
        "data": data
    }), status_code


# GET all
@book_bp.route('/', methods=['GET'])
def get_all():
    try:
        # Lấy danh sách object từ DB
        books = Book.query.all()
        
        # Chuyển đổi toàn bộ object thành dictionary
        books_data = [book.to_dict() for book in books]
        
        return send_response(
            data=books_data, 
            message="Successfully retrieved the list of books!", 
            status_code=200
        )
    except Exception as e:
        # Bắt lỗi an toàn nếu DB có vấn đề
        return send_response(
            data=None, 
            message=f"Error retrieving books: {str(e)}", 
            status_code=500
        )

# POST
@book_bp.route('/', methods=['POST'])
def create():
    data = request.json
    # Danh sách các trường bắt buộc
    required_fields = ['isbn', 'title', 'total_copies']
    
    # Kiểm tra xem có thiếu trường nào không
    missing = [field for field in required_fields if field not in data]
    if missing:
        return send_response(
            success = False,
            message = "Missing data in " + ", ".join(missing) + "!",
            status_code=400
        )
    
    new_book = Book(
        isbn=data.get('isbn'), 
        title=data.get('title'), 
        author=data.get('author'), 
        total_copies=data.get('total_copies', 1), 
        available_copies=data.get('total_copies', 1)
    )
    
    # Lưu vào database
    db.session.add(new_book)
    db.session.commit()

    return send_response(data=new_book.to_dict(), message="New book added successfully!", status_code=201)