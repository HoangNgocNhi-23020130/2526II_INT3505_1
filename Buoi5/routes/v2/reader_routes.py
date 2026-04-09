from flask import Blueprint, request, jsonify
from core.database import db
from models.readers import Reader

# Tạo một Blueprint cho books
reader_bp = Blueprint('readers_v2', __name__)
# Hàm chuẩn hóa Response
def send_response(success=True, data=None, meta = None, message="", status_code=200):
    return jsonify({
        "success": success,
        "message": message,
        "data": data,
        "meta": meta
    }), status_code


@reader_bp.route('/', methods=['GET'])
def get_all():
    try:
        # Lấy tham số phân trang từ URL (mặc định trang 1, 10 người/trang)
        page = request.args.get('page', default=1, type=int)
        size = request.args.get('size', default=10, type=int)

        # Sử dụng paginate() của SQLAlchemy
        pagination = Reader.query.paginate(page=page, per_page=size, error_out=False)
        readers = pagination.items
        
        # Chuyển đổi toàn bộ object thành dictionary
        readers_data = [reader.to_dict() for reader in readers]
        
        meta = {
            "current_page": pagination.page,
            "size": pagination.per_page,
            "total_pages": pagination.pages,
            "total_items": pagination.total,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
            }

        return send_response(
            data=readers_data, 
            meta=meta,
            message="Successfully retrieved the list of readers!", 
            status_code=200
        )
    except Exception as e:
        # Bắt lỗi an toàn nếu DB có vấn đề
        return send_response(
            data=None, 
            message=f"Error retrieving reader: {str(e)}", 
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
            success = False,
            message = "Missing data in " + ", ".join(missing) + "!",
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

    return send_response(data=new_reader.to_dict(), message="New reader added successfully!", status_code=201)