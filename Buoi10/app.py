from prometheus_client import generate_latest
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
from extensions import limiter, metrics
from routes import api_bp
from werkzeug.exceptions import HTTPException

def create_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False

    # 1. Khởi tạo (gắn) limiter vào app
    limiter.init_app(app)
    # Khởi tạo Prometheus và cấu hình endpoint mặc định là /metrics
    metrics.init_app(app)

    # 2. Đăng ký các API từ Blueprint
    app.register_blueprint(api_bp, url_prefix='/api')

    # 3. THIẾT LẬP LOGGING
    setup_logging(app)

    # 4. Xử lý lỗi hệ thống
    register_error_handlers(app)

    return app

def setup_logging(app):
    # Cấu hình file log: tối đa 5MB/file, giữ lại 3 file cũ nhất
    file_handler = RotatingFileHandler('app_production.log', maxBytes=5000000, backupCount=3, encoding='utf-8')
    
    # Định dạng dòng log: [Thời gian] MỨC_ĐỘ in module: Nội dung
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Gắn handler vào logger của Flask và đặt mức độ log (INFO trở lên)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    # Tự động ghi log TRƯỚC mỗi request
    @app.before_request
    def log_request_info():
        app.logger.info(f"Yêu cầu đến: {request.method} {request.url} | IP: {request.remote_addr}")

    # Tự động ghi log SAU mỗi request
    @app.after_request
    def log_response_info(response):
        app.logger.info(f"Phản hồi: {response.status_code}")
        return response

def register_error_handlers(app):
    @app.errorhandler(429)
    def ratelimit_handler(e):
        app.logger.warning(f"Người dùng bị chặn do Rate Limit: {request.remote_addr}")
        return jsonify({"error": f"Bạn đã gửi quá nhiều yêu cầu: {e.description}"}), 429

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({"error": e.description}), e.code
        # Ghi log toàn bộ traceback của lỗi (exc_info=True)
        app.logger.error(f"Lỗi hệ thống không mong muốn: {str(e)}", exc_info=True)
        return jsonify({"error": "Đã xảy ra lỗi hệ thống (500)."}), 500

# Khởi tạo ứng dụng
app = create_app()

if __name__ == '__main__':
    # Chạy server ở chế độ debug
    app.run(debug=True)