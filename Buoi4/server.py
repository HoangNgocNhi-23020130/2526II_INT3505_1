from flask import Flask, jsonify, Blueprint
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
def get_books():
    return send_response(data=books, message="Successfully retrieved the list of books!", status_code=200)

if __name__ == '__main__':
    app.run(debug=True, port = 1604)