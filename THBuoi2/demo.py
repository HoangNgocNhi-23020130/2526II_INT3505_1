import jwt
import datetime
from flask import Flask, jsonify, request, make_response
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JWT_key'

# Database
users_db = {
    "Nguyen Van A": {"password": "123", "role": "Admin"},
    "Tran Thi B": {"password": "hihi", "role": "Reader"},
    "Hoang Ngoc Nhi":{"password": "0810", "role": "Admin"}
}

books_db = [
    {"id": 1, "title": "De Men Phieu Luu Ky", "author": "To Hoai"},
    {"id": 2, "title": "Luoc Su Thoi Gian", "author": "Stephen Hawking"},
    {"id": 3, "title": "Khong Gia Dinh", "author": "Hector Malot"},
    {"id": 4, "title": "Dat Rung Phuong Nam", "author": "To Hoai"}
]

# Phản hồi nhất quán
def lib_res(status, data=None, message=None, code=200):
    return jsonify({"status": status, "data": data, "message": message}), code

# Lấy token từ Header
def parse_bearer_token() -> str | None:
    auth = request.headers.get("Authorization") or ""
    parts = auth.split()
    # Kiểm tra xem có đúng định dạng: Bearer <token> không
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None

# Giải mã token
def decode_token(token: str) -> dict:
    # Trả về nội dung bên trong token (claims)
    return jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

# Check
def require_jwt(required_role: str | None = None):
    token = parse_bearer_token()
    if not token:
        return None, lib_res("error", message="Token is missing!", code=401)
    
    try:
        claims = decode_token(token)
    except jwt.ExpiredSignatureError:
        return None, lib_res("error", message="Token is expired!", code=401)
    except jwt.InvalidTokenError:
        return None, lib_res("error", message="Token is invalid!", code=401)

    # Kiểm tra phân quyền (Role)
    if required_role and claims.get("role") != required_role:
        return None, lib_res("error", message="Permission denied!", code=403)
    
    return claims, None
# Login
@app.post("/api/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return lib_res("error", message="Username and password are required", code=400)

    user = users_db.get(username)
    if not user or user["password"] != password:
        return lib_res("error", message="Invalid credentials", code=401)

    # Tạo JWT (Stateless)
    token = jwt.encode({
        "sub": username,
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({
        "token": token,
        "user": {"username": username, "role": user["role"]}
    }), 200

# Lấy danh sách sách (Public)
@app.route('/api/books', methods=['GET'])
def get_books():
    return lib_res("success", data=books_db)

# Thêm sách mới (Chỉ Admin)
@app.route('/api/books', methods=['POST'])
def add_book():
    current_user, error_res = require_jwt(required_role = "Admin")
    
    if error_res:
        return error_res

    # Lấy dữ liệu từ Request
    data = request.get_json(silent=True) or {}
    title = data.get('title')
    author = data.get('author')

    if not title or not author:
        return lib_res("error", message="Need title and author!", code=400)
    new_book = {
        "id": len(books_db) + 1,
        "title": title,
        "author": author,
    }
    books_db.append(new_book)

    return lib_res("success", data=books_db, message="Book added!", code=201)


# Server: Start
if __name__ == '__main__':
    app.run(debug=True, port=1604)