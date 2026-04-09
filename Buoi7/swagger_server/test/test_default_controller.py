# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.product_input import ProductInput  # noqa: E501
from swagger_server.models.product_response import ProductResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_app_create_product(self):
        """Test case for app_create_product

        Tạo sản phẩm mới
        """
        body = ProductInput()
        response = self.client.open(
            '/products',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_delete_product(self):
        """Test case for app_delete_product

        Xóa sản phẩm
        """
        response = self.client.open(
            '/products/{product_id}'.format(product_id='product_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_get_product(self):
        """Test case for app_get_product

        Lấy thông tin 1 sản phẩm
        """
        response = self.client.open(
            '/products/{product_id}'.format(product_id='product_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_app_get_products(self):
        """Test case for app_get_products

        Lấy danh sách sản phẩm
        """
        response = self.client.open(
            '/products',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
