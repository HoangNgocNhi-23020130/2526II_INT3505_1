from flask import Flask, jsonify
from extensions import limiter
from routes import api_bp

def create_app():
    app = Flask(__name__)

    # 1. Khởi tạo (gắn) limiter vào app
    limiter.init_app(app)

    # 2. Đăng ký các API từ Blueprint
    app.register_blueprint(api_bp, url_prefix='/api')

    # 3. Bắt lỗi 429 (Too Many Requests) khi vượt quá rate limit
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({"error": f"Bạn đã gửi quá nhiều yêu cầu: {e.description}"}), 429

    return app

# Khởi tạo ứng dụng
app = create_app()

if __name__ == '__main__':
    # Chạy server ở chế độ debug
    app.run(debug=True)