from flask import Flask, jsonify, request

app = Flask(__name__)



# Giả lập database nhiều dữ liệu
books_db = [{"id": i, "title": f"Book {i}",
             "author_id": 100+i, "category": "Fiction"} for i in range(1, 51)]
authors_db = [
    {"id": 101, "name": "To Hoai"},
    {"id": 102, "name": "Stephen Hawking"},
    {"id": 103, "name": "Hector Malot"}
]

# Các phản hồi đều nhất quán
# Thêm tham số 'meta' để chứa thông tin phân trang,
# giúp API dễ mở rộng với các tập dữ liệu lớn
def library_response(status, data=None, message=None, meta=None, code=200):
    response = {
        "status": status,
        "data": data,
        "message": message
    }
    if meta:
        response["meta"] = meta
    return jsonify(response), code

# Endpoint cho Books
# Tính dễ hiểu trong lọc dữ liệu: Client truyền tham số gì trong URL thì lọc đó
@app.route('/api/v4/books', methods=['GET'])
def get_books():
    # Lấy tham số lọc từ URL: ?category=Science
    category = request.args.get('category')

    # Mỗi trang 10 cuốn sách
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    filtered_books = books_db
    if category:
        filtered_books = [b for b in books_db if b['category'].lower() == category.lower()]

    # Phân trang dữ liệu
    total_books = len(filtered_books)
    start = (page - 1) * limit
    end = start + limit
    paginated_data = filtered_books[start:end]

    meta = {
        "current_page": page,
        "limit": limit,
        "total_books": total_books,
        "total_pages": (total_books + limit - 1) // limit if limit > 0 else 1
    }
    
    return library_response(
        "success", 
        data=paginated_data, 
        meta=meta,
        message=f"Found {total_books} books"
    )
### Quy tắc đặt tên: Resource ID nằm trong URL sau danh từ số nhiều
@app.route('/api/v4/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books_db if b["id"] == book_id), None)
    if book:
        return library_response("success", data=book)
    
    return library_response("error", message="Not Found", code=404)

# Endpoint cho Authors
# Cấu trúc URL cho Authors tương tự như Books
# Quy tác đặt tên: Danh từ số nhiều, chữ thường
@app.route('/api/v4/authors', methods=['GET'])
def get_authors():
    return library_response("success", data=authors_db)

@app.route('/api/v4/authors', methods=['POST'])
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
# Quy tắc đặt tên: Thể hiện quan hệ phân cấp: sách của tác giả
@app.route('/api/v4/authors/<int:author_id>/books', methods=['GET'])
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