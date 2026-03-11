from flask import Flask, jsonify, request

app = Flask(__name__)

# Database
books_db = [
    {"id": 1, "title": "De Men Phieu Luu Ky", "author_id": 101, "category": "Fiction"},
    {"id": 2, "title": "Luoc Su Thoi Gian", "author_id": 102, "category": "Science"},
    {"id": 3, "title": "Khong Gia Dinh", "author_id": 103, "category": "Fiction"},
    {"id": 4, "title": "Dat Rung Phuong Nam", "author_id": 101, "category": "Fiction"}
] # Thêm thể loại để lọc
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
# Tính dễ hiểu trong lọc dữ liệu: Client truyền tham số gì trong URL thì lọc đó
@app.route('/api/books', methods=['GET'])
def get_books():
    # Lấy tham số lọc từ URL: ?category=Science
    category = request.args.get('category')
    
    if category:
        filtered_books = [b for b in books_db if b['category'].lower() == category.lower()]
        return library_response("success", data=filtered_books)
    
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

# Tính dễ hiểu trong quan hệ giữa các tài nguyên
@app.route('/api/authors/<int:author_id>/books', methods=['GET'])
def get_books_by_author(author_id):
    """
    Ý của URL: 'Lấy các cuốn sách CỦA tác giả có ID này'.
    Thay vì dùng: /api/getBooksByAuthorID?id=101
        -> Trông khó hiểu, không nhất quán với các tác vụ khác tương tự
    """
    author_books = [b for b in books_db if b['author_id'] == author_id]
    
    if not author_books:
        return library_response("error", message="Not Found", code=404)
        
    return library_response("success", data=author_books)

if __name__ == '__main__':
    app.run(debug=True, port=1604)