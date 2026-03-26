from flask import Blueprint, request, jsonify
from core.database import db
from models.readers import Reader

# Tạo một Blueprint cho books
reader_bp = Blueprint('readers', __name__)
# Hàm chuẩn hóa Response
def send_response(success=True, data=None, message="", status_code=200):
    return jsonify({
        "success": success,
        "message": message,
        "data": data
    }), status_code

@reader_bp.route('/', methods=['GET'])
def get_all():
    try:
        # Lấy danh sách object từ DB
        readers = Reader.query.all()
        
        # Chuyển đổi toàn bộ object thành dictionary
        readers_data = [readers.to_dict() for reader in readers]
        
        return send_response(
            data=readers_data, 
            message="Successfully retrieved the list of readers!", 
            status_code=200
        )
    except Exception as e:
        # Bắt lỗi an toàn nếu DB có vấn đề
        return send_response(
            data=None, 
            message=f"Error retrieving books: {str(e)}", 
            status_code=500
        )

@reader_bp.route('/', methods=['POST'])
def create():
    data = request.json
    # Danh sách các trường bắt buộc
    required_fields = ['name', 'email', 'phone']
    
    # Kiểm tra xem có thiếu trường nào không
    missing = [field for field in required_fields if field not in data]
    if missing:
        return send_response(
            status = False,
            message = "Missing data in " + missing + "!",
            status_code=400
        )
    
    new_reader = Reader(
        name=data.get('name'), 
        email=data.get('email'), 
        phone=data.get('phone'), 
    )
    
    # Lưu vào database
    db.session.add(new_reader)
    db.session.commit()

    reader_data = {
        "id": new_reader.id,
        "isbn": new_reader.name,
        "title": new_reader.email,
        "author": new_reader.phone,
        "total_copies": new_reader.membership_date
    }
    return send_response(data=reader_data, message="New reader added successfully!", status_code=201)