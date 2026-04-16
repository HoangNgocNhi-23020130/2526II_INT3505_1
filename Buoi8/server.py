from flask import Flask, jsonify, request

app = Flask(__name__)



# Giả lập database
books = [
    {"id": 1, "title": "Flask cơ bản", "author": "John Doe"},
    {"id": 2, "title": "API Testing", "author": "Jane Smith"}
]

# Các phản hồi đều nhất quán
def library_response(status = "success", data=None, message=None, code=200):
    response = {
        "status": status,
        "data": data,
        "message": message
    }
    return jsonify(response), code

# 1. GET ALL
@app.route('/api/books', methods=['GET'])
def get_books():
    return library_response(data = books)

# 2. GET BY ID
@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return library_response(data = book, message = "Here your book")
    return library_response(status = "error", message = "Book not found", code = 404)

# 3. POST
@app.route('/api/books', methods=['POST'])
def create_book():
    new_book = request.get_json()
    new_book["id"] = len(books) + 1
    books.append(new_book)
    return library_response( data = new_book, message="Created!", code = 201)

# 4. PUT
@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        data = request.get_json()
        book.update(data)
        return library_response(data = book, message = "Done!")
    return library_response(status = "error", message = "Book not found", code = 404)

# 5. DELETE (Xóa)
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return library_response(message = "Deleted!")


if __name__ == '__main__':
    app.run(debug=True, port=1604)