from flask import Blueprint, jsonify
from extensions import limiter

# Tạo Blueprint để gom nhóm các API
api_bp = Blueprint('api', __name__)

@api_bp.route("/public")
def public_api():
    # API này không có decorator riêng, nên sẽ ăn theo default_limits (50 req/giờ)
    return jsonify({"message": "API này giới hạn 50 request/giờ theo mặc định."})

@api_bp.route("/sensitive")
@limiter.limit("3 per minute") # Ghi đè giới hạn: chỉ cho phép 3 request/phút
def sensitive_api():
    return jsonify({"message": "API này chỉ cho phép 3 request/phút. Thử F5 liên tục để test nhé!"})