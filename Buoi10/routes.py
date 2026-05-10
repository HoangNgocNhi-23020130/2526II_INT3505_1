from flask import Blueprint, jsonify, current_app
from extensions import limiter

# Tạo Blueprint để gom nhóm các API
api_bp = Blueprint('api', __name__)

@api_bp.route("/public")
def public_api():
    # Ghi log cấp độ INFO
    current_app.logger.info("Một người dùng vừa truy cập API public.")
    # API này không có decorator riêng, nên sẽ ăn theo default_limits (50 req/giờ)
    return jsonify({"message": "API này giới hạn 50 request/giờ theo mặc định."})

@api_bp.route("/sensitive")
@limiter.limit("3 per minute") # Ghi đè giới hạn: chỉ cho phép 3 request/phút
def sensitive_api():
    # Ghi log cấp độ WARNING (cảnh báo)
    current_app.logger.warning("Truy cập vào API nhạy cảm!")
    return jsonify({"message": "API này chỉ cho phép 3 request/phút. Thử F5 liên tục để test nhé!"})

@api_bp.route("/error")
def trigger_error():
    # Endpoint này cố tình tạo lỗi để test chức năng ghi log lỗi
    current_app.logger.info("Đang cố gắng thực hiện một phép tính nguy hiểm...")
    1 / 0  # Lỗi chia cho 0
    return jsonify({"message": "Sẽ không bao giờ chạy đến dòng này"})