import uuid

def payment_response(status="success", data=None, message=None):
    return {
        "status": status,
        "data": data,
        "message": message
    }

def process_payment(amount, currency):
    """
    Logic lõi xử lý thanh toán. Luôn yêu cầu cả amount và currency.
    """
    if amount <= 0:
        return payment_response(status="error", message="Số tiền không hợp lệ"), 400
        
    # Giả lập gọi sang Cổng thanh toán (Payment Gateway)
    transaction_id = str(uuid.uuid4())
    
    return payment_response(
        data={
            "transaction_id": transaction_id,
            "amount": amount
        },
        message=f"Thanh toan thanh cong {amount} {currency}"
    ), 200