from swagger_server.__main__ import db

class ProductDB(db.Document):
    meta = {'collection': 'products'}
    name = db.StringField(required=True)
    price = db.FloatField(required=True)
    description = db.StringField()