import connexion
import six

from swagger_server.models.product_input import ProductInput  # noqa: E501
from swagger_server.models.product_response import ProductResponse  # noqa: E501
from swagger_server import util


def app_create_product(body):  # noqa: E501
    """Tạo sản phẩm mới

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = ProductInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def app_delete_product(product_id):  # noqa: E501
    """Xóa sản phẩm

     # noqa: E501

    :param product_id: 
    :type product_id: str

    :rtype: None
    """
    return 'do some magic!'


def app_get_product(product_id):  # noqa: E501
    """Lấy thông tin 1 sản phẩm

     # noqa: E501

    :param product_id: 
    :type product_id: str

    :rtype: ProductResponse
    """
    return 'do some magic!'


def app_get_products():  # noqa: E501
    """Lấy danh sách sản phẩm

     # noqa: E501


    :rtype: List[ProductResponse]
    """
    return 'do some magic!'
