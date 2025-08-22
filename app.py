from flask import Flask
from flask_cors import CORS
from routes.product_routes import product_bp
from routes.user_routes import user_bp
from routes.order_routes import order_bp
from routes.cart_routes import cart_bp
from routes.orderdetail_routes import orderdetail_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(product_bp, url_prefix="/api/products")
app.register_blueprint(user_bp, url_prefix="/api/users")
app.register_blueprint(order_bp, url_prefix="/api/orders")
app.register_blueprint(cart_bp, url_prefix="/api/cart")
app.register_blueprint(orderdetail_bp, url_prefix="/api/orderdetails")

@app.route("/")
def home():
    return {"message": "ShoeStore API is running"}

if __name__ == "__main__":
    app.run(debug=True)
