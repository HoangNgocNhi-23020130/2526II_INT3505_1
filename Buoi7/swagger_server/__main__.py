#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from flask_mongoengine import MongoEngine

db = MongoEngine()

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Product Catalog API'}, pythonic_params=True)
    
    app.app.config['MONGODB_SETTINGS'] = {
        'db': 'shop_database',
        'host': 'localhost',
        'port': 27017
    }
    db.init_app(app.app)

    app.run(port=8080)


if __name__ == '__main__':
    main()
