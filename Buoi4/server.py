from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)

app.config['SWAGGER'] = {
    'openapi': '3.0.0'
}

# Kết nối trực tiếp đến file YAML bên ngoài
swagger = Swagger(app, template_file='swagger.yaml')

# Database in-memory
books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "isbn": "978-0132350884"},
    {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "isbn": "978-0135957059"}
]

# Hàm chuẩn hóa Response
def send_response(success=True, data=None, message="", status_code=200):
    return jsonify({
        "success": success,
        "message": message,
        "data": data
    }), status_code

@app.route('/v1/books', methods=['GET'])
@app.route('/v2/books', methods=['GET'])
@app.route('/v3/books', methods=['GET'])
def get_books():
    return send_response(data=books, message="Successfully retrieved the list of books!", status_code=200)

@app.route('/v2/books', methods=['POST'])
@app.route('/v3/books', methods=['POST'])
def add_book():
    data = request.json
    if not data or 'title' not in data or 'author' not in data or 'isbn' not in data:
        return send_response(success=False, message="Missing required data!", status_code=400)
    
    new_book = {
        "id": books[-1]['id'] + 1 if books else 1,
        "title": data['title'],
        "author": data['author'],
        "isbn": data['isbn']
    }
    books.append(new_book)
    return send_response(data=new_book, message="New book added successfully!", status_code=201)

@app.route('/v3/books/<int:id>', methods=['GET'])
def get_book(id):
    book = next((b for b in books if b['id'] == id), None)
    if not book:
        return send_response(success=False, message="Not found!", status_code=404)
    return send_response(data=book, message="Successfully retrieved a book!", status_code=200)

if __name__ == '__main__':
    app.run(debug=True, port = 1604)