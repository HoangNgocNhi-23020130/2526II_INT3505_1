from flask import Blueprint, request, jsonify
from core.database import db
from models.borrow_records import BorrowRecord
from models.books import Book
from datetime import datetime, timedelta

borrow_bp = Blueprint('borrow-records', __name__)

# Hàm chuẩn hóa Response
def send_response(success=True, data=None, meta=None, message="", status_code=200):
    return jsonify({
        "success": success,
        "message": message,
        "data": data,
        "meta": meta
    }), status_code

# GET all
@borrow_bp.route('/', methods=['GET'])
def get_reader_borrows(rid):
    try:
        # Lấy tham số cursor và limit từ URL (mặc định cursor=0 lấy từ đầu, limit=10)
        cursor = request.args.get('cursor', default=0, type=int)
        limit = request.args.get('limit', default=10, type=int)
        
        # Truy vấn DB: Lấy các bản ghi của độc giả (rid) có id > cursor, sắp xếp tăng dần
        records = BorrowRecord.query.filter(
            BorrowRecord.reader_id == rid,
            BorrowRecord.id > cursor
        ).order_by(BorrowRecord.id.asc()).limit(limit).all()
        
        # Xác định cursor tiếp theo (ID của bản ghi cuối cùng trong danh sách)
        next_cursor = records[-1].id if records else None
        
        # Chuyển đổi toàn bộ object thành dictionary
        records_data = [rec.to_dict() for rec in records]

        meta = {
            "next_cursor": next_cursor,
            "limit": limit,
            "has_more": next_cursor is not None
        }
        
        return send_response(
            data=records_data, 
            meta=meta,
            message="Successfully retrieved the list of borrow records!", 
            status_code=200
        )
    except Exception as e:
        # Bắt lỗi an toàn nếu DB có vấn đề
        return send_response(
            data=None, 
            message=f"Error retrieving records: {str(e)}", 
            status_code=500
        )

# POST Mượn sách
@borrow_bp.route('/', methods=['POST'])
def borrow_book(rid):
    data = request.json
    book = Book.query.get(data['book_id'])
    
    if not book or book.available_copies <= 0:
        return send_response(
            success=False,
            message="Not available!",
            status_code=400)
        
    new_record = BorrowRecord(
        reader_id=rid,
        book_id=book.id,
        due_date=datetime.utcnow() + timedelta(days=14),
        status='borrowed'
    )
    book.available_copies -= 1
    db.session.add(new_record)
    db.session.commit()

    return send_response(data=new_record.to_dict(), message="Borrow successfull!", status_code=201)

# PATCH Trả sách
@borrow_bp.route('/<int:id>', methods=['PATCH'])
def return_book(rid, id):
    record = BorrowRecord.query.filter_by(id=id, reader_id=rid).first()
    if not record or record.status != 'borrowed':
        return send_response(
            success=False,
            message="Can not return!",
            status_code=400)
        
    record.status = 'returned'
    record.return_date = datetime.utcnow()
    
    book = Book.query.get(record.book_id)
    book.available_copies += 1
    
    db.session.commit()
    return send_response(message="Return successfull!", status_code=200)