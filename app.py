from flask import Flask
from flask_cors import CORS

# Tạo app Flask
app = Flask(__name__)
CORS(app)

# Import routes
from routes import user_routes, product_routes, order_routes
app.register_blueprint(user_routes.bp, url_prefix="/api/users")
app.register_blueprint(product_routes.bp, url_prefix="/api/products")
app.register_blueprint(order_routes.bp, url_prefix="/api/orders")

if __name__ == "__main__":
    app.run(debug=True)