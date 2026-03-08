from flask import Flask, jsonify, request, make_response
import time

app = Flask(__name__)

# Database
users_db = [
    {"id": 1, "name": "Nguyen Van A", "role": "Admin"},
    {"id": 2, "name": "Tran Thi B", "role": "Editor"},
    {"id": 3, "name": "Hoang Ngoc Nhi", "role": "Editor"}
]

@app.route('/api/users', methods=['GET'])
def get_user_heavy_data():
    # Giả lập một tác vụ tốn thời gian (truy vấn DB lớn, tính toán phức tạp...)
    # Cần chờ 10s để có thể tải hoàn tất dữ liệu
    time.sleep(10) 
    
    response = make_response(jsonify({
        "status": "success",
        "message": "Đây là dữ liệu nặng đã xử lý xong!",
        "data": users_db,
        "timestamp": time.time()
    }
    ))
    
    # Thiết lập Cache trong 60 giây. 
    # 'public': Cho phép cả trình duyệt và các Proxy lưu cache.
    # 'max-age=60': Dữ liệu có hiệu lực trong 60s.
    response.headers['Cache-Control'] = 'public, max-age=60'
    
    return response

@app.route('/api/users', methods=['POST'])
def post_users():
    new_users = {"id": len(users_db) + 1,
                 "name": request.json['name'],
                 "role": request.json['role']}
    users_db.append(new_users)
    return jsonify(new_users), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def changeall_users(user_id):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if user:
        user['name'] = request.json['name']
        user['role'] = request.json['role']
        return jsonify({"message": "Updated full user", "data": user})
    return jsonify({"error": "Not found"}), 404

@app.route('/api/users/<int:user_id>', methods=['PATCH'])
def update_user_partial(user_id):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if user:
        if 'name' in request.json:
            user['name'] = request.json['name']
        if 'role' in request.json:
            user['role'] = request.json['role']
        return jsonify({"message": "Partial update success", "data": user})
    return jsonify({"error": "Not found"}), 404

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users_db
    users_db = [u for u in users_db if u["id"] != user_id]
    return jsonify({"message": f"User {user_id} deleted"}), 200

# Server: Start
if __name__ == '__main__':
    app.run(debug=True, port=1604)