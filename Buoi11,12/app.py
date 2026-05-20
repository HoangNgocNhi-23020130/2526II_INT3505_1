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
if __name__ == '__main__':
    app.run(debug=True, port=5000)