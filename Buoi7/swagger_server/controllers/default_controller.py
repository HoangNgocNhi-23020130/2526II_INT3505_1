import connexion
import six

from swagger_server.models.product_input import ProductInput  # noqa: E501
from swagger_server.models.product_response import ProductResponse  # noqa: E501
from swagger_server import util
from swagger_server.models.db_models import ProductDB
from bson.objectid import ObjectId


def app_create_product(body):  # noqa: E501
    """Tạo sản phẩm mới

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        # Lấy dữ liệu user gửi lên
        data = connexion.request.get_json() 
        
        # Lưu vào MongoDB
        new_product = ProductDB(
            name=data['name'],
            price=data['price'],
            description=data.get('description', '')
        )
        new_product.save()
        return {"message": "Thành công", "id": str(new_product.id)}, 201
    return "Dữ liệu không hợp lệ", 400


def app_delete_product(product_id):  # noqa: E501
    """Xóa sản phẩm

     # noqa: E501

    :param product_id: 
    :type product_id: str

    :rtype: None
    """
    # Tìm sản phẩm trong DB
    product = ProductDB.objects(id=product_id).first()
    
    # Nếu không tìm thấy
    if not product:
        return "Không tìm thấy sản phẩm để xóa", 404
        
    # Xóa sản phẩm khỏi database
    product.delete()
    
    return "Xóa sản phẩm thành công", 204


def app_get_product(product_id):  # noqa: E501
    """Lấy thông tin 1 sản phẩm

     # noqa: E501

    :param product_id: 
    :type product_id: str

    :rtype: ProductResponse
    """
    product = ProductDB.objects(id=product_id).first()
    
    # Nếu không tìm thấy, trả về lỗi 404
    if not product:
        return "Không tìm thấy sản phẩm", 404
        
    # Nếu tìm thấy, trả về thông tin sản phẩm và mã 200 (OK)
    return {
        "id": str(product.id),
        "name": product.name,
        "price": product.price,
        "description": product.description
    }, 200

def app_get_products():  # noqa: E501
    """Lấy danh sách sản phẩm

     # noqa: E501


    :rtype: List[ProductResponse]
    """
    products = ProductDB.objects()
    result = []
    for p in products:
        result.append({
            "id": str(p.id),
            "name": p.name,
            "price": p.price,
            "description": p.description
        })
    return result, 200
