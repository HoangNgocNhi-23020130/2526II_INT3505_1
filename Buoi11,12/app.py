from flask import Flask, request, jsonify, url_for
import threading
import time
import hmac
import hashlib
import json
import uuid

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Laptop", "category": "electronics", "price": 1000, "created_at": "2023-01-01"},
    {"id": 2, "name": "Mouse", "category": "electronics", "price": 50, "created_at": "2023-01-02"},
    {"id": 3, "name": "Desk", "category": "furniture", "price": 200, "created_at": "2023-01-03"}
]

WEBHOOK_SUBSCRIPTIONS = []
WEBHOOK_SECRET = "my_super_secret_key"  # Dùng để tạo HMAC Signature

def app_response(status, data=None, message=None, code=200):
    response = {
        "status": status,
        "data": data,
        "message": message
    }
    return jsonify(response), code

# ==========================================
# 1 & 2. CRUD & QUERY PATTERN (Lọc, Sắp xếp, Phân trang)
# ==========================================
@app.route('/api/v1/products', methods=['GET'])
def get_products():
    """
    Demo Query Pattern: Lọc theo category, sắp xếp theo giá, phân trang Offset.
    """
    category = request.args.get('category')
    sort = request.args.get('sort')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 2))
    
    results = PRODUCTS.copy()
    
    # Filtering (Lọc)
    if category:
        results = [p for p in results if p['category'] == category]
        
    # Sorting (Sắp xếp)
    if sort == '-price':
        results = sorted(results, key=lambda x: x['price'], reverse=True)
    elif sort == 'price':
        results = sorted(results, key=lambda x: x['price'])
        
    # Pagination (Phân trang Offset-based)
    start = (page - 1) * limit
    end = start + limit
    paginated_results = results[start:end]

    return app_response(
        status="success",
        message="Products retrieved successfully",
        data={
            "items": paginated_results,
            "meta": {
                "page": page,
                "limit": limit,
                "total": len(results)
            }
        }
    )

# ==========================================
# 3. HATEOAS PATTERN
# ==========================================
@app.route('/api/v1/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Demo HATEOAS: Trả về dữ liệu kèm theo các 'links' để client biết bước tiếp theo.
    """
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return jsonify({"error": "Not found"}), 404
        
    response_data = product.copy()
    
    # Thêm điều hướng Hypermedia
    response_data['links'] = [
        {"rel": "self", "href": f"/api/v1/products/{product_id}", "method": "GET"},
        {"rel": "buy", "href": "/api/v1/orders", "method": "POST"}
    ]
    
    return app_response(
        status="success", 
        message="Product details retrieved successfully", 
        data=response_data
    )

# ==========================================
# 4. EVENT-DRIVEN PATTERN (Xử lý bất đồng bộ)
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
            "links": [
                {"rel": "check_status", "href": f"/api/v1/tasks/{task_id}", "method": "GET"}
            ]
        },
        code=202
    )

def background_order_processing(task_id, data):
    print(f"[Worker] Đang xử lý đơn hàng cho task {task_id}...")
    time.sleep(5)  # Mô phỏng tác vụ nặng
    print(f"[Worker] Xử lý xong task {task_id}!")
    
    # Sau khi xong, gọi Webhook để thông báo
    trigger_webhook("order.completed", {"task_id": task_id, "status": "success", "order_data": data})

# ==========================================
# 5. WEBHOOK PATTERN (Real-time Notification & HMAC Security)
# ==========================================
@app.route('/api/v1/webhooks/subscribe', methods=['POST'])
def subscribe_webhook():
    """Client đăng ký URL để nhận sự kiện"""
    data = request.json or {}
    endpoint_url = data.get('endpoint_url')
    
    if not endpoint_url:
        return app_response(
            status="error",
            message="Missing 'endpoint_url' in request body",
            code=400
        )
    
    WEBHOOK_SUBSCRIPTIONS.append({
        "id": str(uuid.uuid4()),
        "endpoint_url": endpoint_url,
        "event_types": ["order.completed"]
    })
    
    return app_response(
        status="success", 
        message="Webhook subscribed successfully!", 
        code=201
    )

def trigger_webhook(event_type, payload):
    """Gửi HTTP POST payload đến các URL đã đăng ký kèm chữ ký bảo mật HMAC"""
    payload_str = json.dumps(payload)
    
    # Tạo chữ ký HMAC-SHA256
    signature = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'), 
        payload_str.encode('utf-8'), 
        hashlib.sha256
    ).hexdigest()
    
    headers = {
        "Content-Type": "application/json",
        "X-Stripe-Signature": signature
    }
    
    for sub in WEBHOOK_SUBSCRIPTIONS:
        if event_type in sub['event_types']:
            print(f"\n[Webhook] Firing POST to {sub['endpoint_url']}")
            print(f"[Webhook] Payload: {payload_str}")
            print(f"[Webhook] Signature: {signature}\n")
            # Thực tế: requests.post(sub['endpoint_url'], json=payload, headers=headers)

if __name__ == '__main__':
    app.run(debug=True, port=5000)