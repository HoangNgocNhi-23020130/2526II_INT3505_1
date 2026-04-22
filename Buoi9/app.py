from flask import Flask
from api.v1.payment_controller import api_v1

app = Flask(__name__)

# Đăng ký blueprint v1
app.register_blueprint(api_v1, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run(debug=True, port=1604)