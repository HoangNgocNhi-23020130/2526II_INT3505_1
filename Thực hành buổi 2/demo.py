from flask import Flask, jsonify

app = Flask(__name__)

# Database
users_db = [
    {"id": 1, "name": "Nguyen Van A", "role": "Admin"},
    {"id": 2, "name": "Tran Thi B", "role": "Editor"},
    {"id": 3, "name": "Hoang Ngoc Nhi", "role": "Editor"}
]

@app.route('/api/users', methods=['GET'])
def get_users():
    """
    Server chỉ trả về dữ liệu thuần túy (JSON). 
    Nó không quan tâm Client sẽ hiển thị bảng, danh sách hay biểu đồ.
    """
    return jsonify({
        "status": "success",
        "data": users_db
    })

# Server: Start
if __name__ == '__main__':
    app.run(debug=True, port=1604)