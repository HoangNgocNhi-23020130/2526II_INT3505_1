from flask import Flask
from flasgger import Swagger
from core.database import db

def create_app():
    app = Flask(__name__)
    # Cấu hình database (Sử dụng SQLite cho demo)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Gắn database và server với nhau
    db.init_app(app)

    app.config['SWAGGER'] = {
    'openapi': '3.0.0'
    }
    swagger = Swagger(app, template_file='swagger.yaml')

    # Tạo bảng tự động khi server được khởi tạo
    with app.app_context():
        # Import các model vào để SQLAlchemy nhận diện
        from models.book import Book
        from models.reader import Reader 
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)