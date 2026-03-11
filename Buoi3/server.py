from flask import Flask, jsonify, request

app = Flask(__name__)

# Database
books_db = [
    {"id": 1, "title": "De Men Phieu Luu Ky", "author_id": 101},
    {"id": 2, "title": "Luoc Su Thoi Gian", "author_id": 102},
    {"id": 3, "title": "Khong Gia Dinh", "author_id": 103}
]
authors_db = [
    {"id": 101, "name": "To Hoai"},
    {"id": 102, "name": "Stephen Hawking"},
    {"id": 103, "name": "Hector Malot"}
]

# Các phản hồi đều nhất quán
def library_response(status, data=None, message=None, code=200):
    """
    Đảm bảo mọi API của Thư viện
    đều trả về cùng một cấu trúc JSON duy nhất.
    """
    return jsonify({
        "status": status,    # 'success' hoặc 'error'
        "data": data,        # Dữ liệu
        "message": message   # Thông báo phản hồi
    }), code # mã phản hồi

# Endpoint cho Books
@app.route('/api/books', methods=['GET'])
def get_books():
    return library_response("success", data=books_db)

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books_db if b["id"] == book_id), None)
    if book:
        return library_response("success", data=book)
    
    return library_response("error", message="Not Found", code=404)

# Endpoint cho Authors
# Cấu trúc URL cho Authors tương tự như Books
@app.route('/api/authors', methods=['GET'])
def get_authors():
    return library_response("success", data=authors_db)

@app.route('/api/authors', methods=['POST'])
def add_author():
    if not request.json or 'name' not in request.json:
        return library_response("error", message="Please write name", code=400)
    
    new_author = {
        "id": authors_db[-1]["id"] + 1 if authors_db else 1,
        "name": request.json.get('name')
    }
    authors_db.append(new_author)
    return library_response("success", data=new_author, message="POST Successful", code=201)

if __name__ == '__main__':
    app.run(debug=True, port=1604)