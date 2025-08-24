from flask import Flask, render_template, session, flash, redirect, url_for, request
from flask_cors import CORS
from routes.product_routes import product_bp
from routes.user_routes import user_bp
from routes.order_routes import order_bp
from db import get_db

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = 'your_secret_key'
CORS(app)

# ================== REGISTER BACKEND BLUEPRINTS ==================
app.register_blueprint(product_bp, url_prefix="/api/products")
app.register_blueprint(user_bp, url_prefix="/api/users")
app.register_blueprint(order_bp, url_prefix="/api/orders")

# ================== HÀM XỬ LÝ GIỎ HÀNG ==================
def get_product_by_id(product_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    return product

def get_cart_items():
    return session.get("cart", [])

def get_cart_total():
    cart = session.get("cart", [])
    return sum(item["price"] * item["quantity"] for item in cart)

def calculate_final_total():
    cart_total = get_cart_total()
    shipping_fee = 30000 if cart_total < 500000 else 0
    promo_discount = 0
    if "applied_promo" in session:
        promo = session["applied_promo"]
        promo_discount = cart_total * promo.get("discount", 0)
        if promo.get("free_ship"):
            shipping_fee = 0
    final_total = cart_total - promo_discount + shipping_fee
    return {
        "cart_total": cart_total,
        "shipping_fee": shipping_fee,
        "promo_discount": promo_discount,
        "final_total": final_total
    }

def get_cart_count():
    return sum(item["quantity"] for item in session.get("cart", []))

def add_to_cart(product_id, size, quantity):
    product = get_product_by_id(product_id)
    if not product:
        return False
    if "cart" not in session:
        session["cart"] = []
    cart = session["cart"]
    for item in cart:
        if item["product_id"] == int(product_id) and item.get("size") == size:
            item["quantity"] += int(quantity)
            session["cart"] = cart
            return True
    cart.append({
        "product_id": int(product_id),
        "name": product["name"],
        "price": product["price"],
        "quantity": int(quantity),
        "size": size,
        "image": product["image"] if "image" in product else ""
    })
    session["cart"] = cart
    return True

# ================== ROUTES FRONTEND ==================
@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return render_template('home.html', products=products, cart_count=get_cart_count())

@app.route('/home')
def home():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return render_template('home.html', products=products, cart_count=get_cart_count())

@app.route('/giohang')
def giohang():
    cart_items = get_cart_items()
    totals = calculate_final_total()
    applied_promo = session.get('applied_promo', None)
    return render_template('giohang.html', 
                         cart_items=cart_items, 
                         cart_total=totals['cart_total'],
                         shipping_fee=totals['shipping_fee'],
                         promo_discount=totals['promo_discount'],
                         final_total=totals['final_total'],
                         applied_promo=applied_promo,
                         cart_count=get_cart_count())

# ================== CHẠY APP ==================
if __name__ == '__main__':
    app.run(debug=True)