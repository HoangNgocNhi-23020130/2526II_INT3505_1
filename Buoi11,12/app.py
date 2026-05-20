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

def app_response(status, data=None, message=None, meta=None, code=200):
    response = {
        "status": status,
        "data": data,
        "message": message
    }
    if meta:
        response["meta"] = meta
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

    meta = {
        "current_page": page,
        "limit": limit,
        "total": len(results)
    }
    
    return app_response(
        status="success", 
        data=paginated_results, 
        meta=meta,
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)