from flask import Flask
from flasgger import Swagger
from core.database import db

from routes.v1.book_routes import book_bp as book_v1_bp
from routes.v1.reader_routes import reader_bp as reader_v1_bp
from routes.v1.borrow_routes import borrow_bp as borrow_v1_bp

from routes.v2.book_routes import book_bp as book_v2_bp

def create_app():
    app = Flask(__name__)
    # Cấu hình database (Sử dụng SQLite cho demo)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Gắn database và server với nhau
    db.init_app(app)

    app.register_blueprint(book_v1_bp, url_prefix='/api/v1/books')
    app.register_blueprint(reader_v1_bp, url_prefix='/api/v1/readers')
    app.register_blueprint(borrow_v1_bp, url_prefix='/api/v1/readers/<int:rid>/borrow-records')

    app.register_blueprint(book_v2_bp, url_prefix='/api/v2/books')

    app.config['SWAGGER'] = {
    'openapi': '3.0.0'
    }
    swagger = Swagger(app, template_file='swagger.yaml')

    # Tạo bảng tự động khi server được khởi tạo
    with app.app_context():
        # Import các model vào để SQLAlchemy nhận diện
        from models.books import Book
        from models.readers import Reader
        from models.borrow_records import BorrowRecord 
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=1604)