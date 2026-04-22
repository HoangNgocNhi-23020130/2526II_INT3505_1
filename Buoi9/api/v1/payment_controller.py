from flask import Blueprint, request, jsonify, make_response
from services.payment_service import process_payment, payment_response

api_v1 = Blueprint('api_v1', __name__)

@api_v1.route('/payments', methods=['POST'])
def create_payment_v1():
    """
    Tạo giao dịch thanh toán (Chỉ hỗ trợ VNĐ)
    """
    
    data = request.get_json()
    
    if not data or 'amount' not in data:
        error_response = payment_response(status="error", message="Thiếu trường 'amount'")
        return jsonify(error_response), 400

    amount = data['amount']
    currency = "VND" 
    
    result_dict, status_code = process_payment(amount, currency)
    
    response = make_response(jsonify(result_dict), status_code)
    
    return response