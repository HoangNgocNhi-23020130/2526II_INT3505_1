from flask import Flask, request, jsonify, url_for
import threading
import time
import hmac
import hashlib
import json
import uuid
import requests

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Laptop", "category": "electronics", "price": 1000, "created_at": "2023-01-01"},
    {"id": 2, "name": "Mouse", "category": "electronics", "price": 50, "created_at": "2023-01-02"},
    {"id": 3, "name": "Desk", "category": "furniture", "price": 200, "created_at": "2023-01-03"}
]

WEBHOOK_SUBSCRIPTIONS = []
WEBHOOK_SECRET = "my_super_secret_key"  # Dùng để tạo HMAC Signature (Giống Stripe/GitHub)

def app_response(status, data=None, message=None, code=200):
    response = {
        "status": status,
        "data": data,
        "message": message
    }
    return jsonify(response), code

# ==========================================
# 1 & 2. CRUD, QUERY & HATEOAS PATTERN
# ==========================================
@app.route('/api/v1/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'GET':
        """
        Demo Query Pattern: Lọc theo category, sắp xếp theo giá, phân trang Offset.
        """
        category = request.args.get('category')
        sort = request.args.get('sort')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 2))
        
        results = PRODUCTS.copy()
        
        # Lọc
        if category:
            results = [p for p in results if p['category'] == category]
            
        # Sắp xếp
        if sort == '-price':
            results = sorted(results, key=lambda x: x['price'], reverse=True)
        elif sort == 'price':
            results = sorted(results, key=lambda x: x['price'])
            
        # Phân trang
        start = (page - 1) * limit
        end = start + limit
        paginated_results = results[start:end]

        # Áp dụng HATEOAS cho list
        for item in paginated_results:
            item['links'] = [{"rel": "self", "href": f"/api/v1/products/{item['id']}", "method": "GET"}]

        return app_response(
            status="success",
            data={
                "items": paginated_results,
                "meta": {"page": page, "limit": limit, "total": len(results)},
                "links": [
                    {"rel": "create", "href": "/api/v1/products", "method": "POST"}
                ]
            }
        )
    
    elif request.method == 'POST':
        """Demo CRUD: Create"""
        data = request.json or {}
        new_id = max(p['id'] for p in PRODUCTS) + 1 if PRODUCTS else 1
        new_product = {
            "id": new_id,
            "name": data.get("name"),
            "category": data.get("category"),
            "price": data.get("price"),
            "created_at": time.strftime("%Y-%m-%d")
        }
        PRODUCTS.append(new_product)
        return app_response(status="success", message="Product created successfully", data=new_product, code=201)

@app.route('/api/v1/products/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_product(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return app_response(status="error", message="Product not found", code=404)

    if request.method == 'GET':
        """Demo HATEOAS: Trả về links để hướng dẫn client"""
        response_data = product.copy()
        response_data['links'] = [
            {"rel": "self", "href": f"/api/v1/products/{product_id}", "method": "GET"},
            {"rel": "update", "href": f"/api/v1/products/{product_id}", "method": "PUT"},
            {"rel": "delete", "href": f"/api/v1/products/{product_id}", "method": "DELETE"},
            {"rel": "buy", "href": "/api/v1/orders", "method": "POST"}
        ]
        return app_response(status="success", data=response_data)
        
    elif request.method == 'PUT':
        """Demo CRUD: Update"""
        data = request.json or {}
        product.update({k: v for k, v in data.items() if k in ['name', 'category', 'price']})
        return app_response(status="success", message="Product updated", data=product)

    elif request.method == 'DELETE':
        """Demo CRUD: Delete"""
        PRODUCTS.remove(product)
        return app_response(status="success", message="Product deleted")

# ==========================================
# 4. EVENT-DRIVEN PATTERN
# ==========================================
@app.route('/api/v1/orders', methods=['POST'])
def create_order():
    """
    Demo Event-driven: Client không cần chờ quá trình xử lý phức tạp.
    Trả về 202 Accepted và task_id ngay lập tức.
    """
    data = request.json or {}
    task_id = str(uuid.uuid4())
    
    # Đẩy vào Background Job
    threading.Thread(target=background_order_processing, args=(task_id, data)).start()
    
    return app_response(
        status="success",
        message="Order is being processed in the background",
        data={
            "task_id": task_id,
            "status": "pending",
            "links": [{"rel": "check_status", "href": f"/api/v1/tasks/{task_id}", "method": "GET"}]
        },
        code=202
    )

def background_order_processing(task_id, data):
    print(f"\n[Worker] Đang xử lý đơn hàng cho task {task_id}...")
    time.sleep(2)  # Mô phỏng tác vụ nặng
    print(f"[Worker] Xử lý xong task {task_id}!")
    
    # Sau khi xong, trigger webhook
    trigger_webhook("order.completed", {"task_id": task_id, "status": "success", "order_data": data})

# ==========================================
# 5. WEBHOOK PATTERN (Mô phỏng Stripe Webhook)
# ==========================================
@app.route('/api/v1/webhooks/subscribe', methods=['POST'])
def subscribe_webhook():
    """Client đăng ký URL để nhận sự kiện"""
    data = request.json or {}
    endpoint_url = data.get('endpoint_url')
    
    if not endpoint_url:
        return app_response(status="error", message="Missing 'endpoint_url' in request body", code=400)
    
    WEBHOOK_SUBSCRIPTIONS.append({
        "id": str(uuid.uuid4()),
        "endpoint_url": endpoint_url,
        "event_types": ["order.completed"]
    })
    
    return app_response(status="success", message="Webhook subscribed successfully!", code=201)

def trigger_webhook(event_type, payload):
    """
    Gửi Webhook với HMAC Signature và Timestamp
    Mô phỏng theo Stripe API Pattern (chống Replay Attack)
    """
    payload_str = json.dumps(payload)
    timestamp = str(int(time.time()))
    
    # Chuỗi để ký: timestamp + '.' + payload (Pattern phổ biến của Stripe)
    signed_payload = f"{timestamp}.{payload_str}"
    
    signature = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'), 
        signed_payload.encode('utf-8'), 
        hashlib.sha256
    ).hexdigest()
    
    # Header chuẩn của Stripe
    stripe_signature_header = f"t={timestamp},v1={signature}"
    
    headers = {
        "Content-Type": "application/json",
        "X-Webhook-Signature": stripe_signature_header
    }
    
    for sub in WEBHOOK_SUBSCRIPTIONS:
        if event_type in sub['event_types']:
            print(f"[Webhook] Firing POST to {sub['endpoint_url']}")
            try:
                # Gửi HTTP POST thực sự (timeout ngắn để khỏi treo)
                requests.post(sub['endpoint_url'], json=payload, headers=headers, timeout=3)
                print(f"[Webhook] Sent successfully!")
            except Exception as e:
                print(f"[Webhook] Failed to send: {e}")

# ==========================================
# TÍCH HỢP HỆ THỐNG: MOCK NOTIFICATION SYSTEM
# (Đóng vai trò hệ thống bên thứ 3 nhận Webhook)
# ==========================================
@app.route('/notification-service/webhook-receiver', methods=['POST'])
def mock_notification_receiver():
    """
    Hệ thống thông báo nhận webhook, xác thực HMAC Signature.
    (Mô phỏng bài toán Tích hợp Webhook vào hệ thống thông báo)
    """
    signature_header = request.headers.get("X-Webhook-Signature", "")
    payload_str = request.get_data(as_text=True)
    
    # Parse header: t=12345,v1=abcdef
    header_parts = dict(part.split('=') for part in signature_header.split(',') if '=' in part)
    timestamp = header_parts.get('t')
    received_signature = header_parts.get('v1')
    
    if not timestamp or not received_signature:
        print("[Notification System] Missing signature parts!")
        return jsonify({"error": "Invalid signature format"}), 400
        
    # Chống Replay Attack: Kiểm tra timestamp không quá 5 phút
    if int(time.time()) - int(timestamp) > 300:
        print("[Notification System] Replay attack detected!")
        return jsonify({"error": "Timestamp expired"}), 400
        
    # Tính lại chữ ký dựa trên secret chia sẻ
    signed_payload = f"{timestamp}.{payload_str}"
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        signed_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(expected_signature, received_signature):
        print("[Notification System] Invalid signature!")
        return jsonify({"error": "Invalid signature"}), 401
        
    # Xử lý sự kiện nếu chữ ký hợp lệ
    payload = request.json
    print(f"[Notification System] Signature VERIFIED.")
    print(f"[Notification System] Sending notification for Event: {payload}")
    return jsonify({"status": "Notification logic executed successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)