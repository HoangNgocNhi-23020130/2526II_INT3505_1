import os
import jwt
import uuid
from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify, request, make_response, g
from functools import wraps
from dotenv import load_dotenv

# Tự động tìm và nạp các biến từ file .env vào os.environ
load_dotenv()

app = Flask(__name__)
# Lấy các biến môi trường
app.config['SECRET_KEY'] = os.getenv('ACCESS_TOKEN_SECRET', 'default_access_secret')
app.config['REFRESH_SECRET_KEY'] = os.getenv('REFRESH_TOKEN_SECRET', 'default_refresh_secret')

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
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = parse_bearer_token()
            if not token:
                return lib_res("error", message="Token is missing!", code=401)
            
            try:
                claims = decode_token(token)
            except jwt.ExpiredSignatureError:
                return lib_res("error", message="Token is expired!", code=401)
            except jwt.InvalidTokenError:
                return lib_res("error", message="Token is invalid!", code=401)

            # Kiểm tra phân quyền (Role)
            if required_role and claims.get("role") != required_role:
                return lib_res("error", message="Permission denied!", code=403)
            
            # Lưu thông tin và cho đi tiếp
            g.current_user = claims
            return f(*args, **kwargs)
        return decorated_function
    return decorator
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

    access_payload = {
        "jti": str(uuid.uuid4()),
        "sub": username,
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    access_token = jwt.encode(access_payload, app.config['SECRET_KEY'], algorithm="HS256")

    refresh_payload = {
        "jti": str(uuid.uuid4()),
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }
    refresh_token = jwt.encode(refresh_payload, app.config['REFRESH_SECRET_KEY'], algorithm="HS256")

    return lib_res("success", data={
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {"username": username, "role": user["role"]}
    }, message="Login successful")

# Refresh Token (Lấy Access Token mới)
@app.post("/api/auth/refresh")
def refresh_token():
    data = request.get_json(silent=True) or {}
    ref_token = data.get("refresh_token")
    
    if not ref_token:
        return lib_res("error", message="Refresh token is required", code=400)
    
    try:
        claims = jwt.decode(ref_token, app.config['REFRESH_SECRET_KEY'], algorithms=["HS256"])
        username = claims.get("sub")
        
        user = users_db.get(username)
        if not user:
            raise jwt.InvalidTokenError

        new_access_payload = {
            "jti": str(uuid.uuid4()),
            "sub": username,
            "role": user["role"],
            "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
        }
        new_access_token = jwt.encode(new_access_payload, app.config['SECRET_KEY'], algorithm="HS256")
        
        return lib_res("success", data={"access_token": new_access_token}, message="Token refreshed")

    except jwt.ExpiredSignatureError:
        return lib_res("error", message="Refresh token expired. Please login again.", code=401)
    except jwt.InvalidTokenError:
        return lib_res("error", message="Invalid refresh token.", code=401)

# Lấy danh sách sách (Public)
@app.route('/api/books', methods=['GET'])
def get_books():
    return lib_res("success", data=books_db)

# Thêm sách mới (Chỉ Admin)
@app.route('/api/books', methods=['POST'])
@require_jwt(required_role="Admin")
def add_book():
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
    app.run(debug=True, port=int(os.getenv('PORT', 1604)))