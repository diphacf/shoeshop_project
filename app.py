from flask import Flask, render_template, session, flash, redirect, url_for, request
from flask_cors import CORS
from routes.product_routes import product_bp
from routes.user_routes import user_bp
from routes.order_routes import order_bp
from db import get_db

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = 'your_secret_key'
CORS(app)

# Đăng ký các blueprint
app.register_blueprint(product_bp, url_prefix="/api/products")
app.register_blueprint(user_bp, url_prefix="/api/users")
app.register_blueprint(order_bp, url_prefix="/api/orders")

# ================== HÀM XỬ LÝ DB ==================
def get_products():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return products

def get_product_by_id(product_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    return product

def get_products_by_category(category):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE category=%s", (category,))
    products = cursor.fetchall()
    cursor.close()
    return products

# ================== ROUTES FRONTEND ==================
@app.route('/')
def index():
    products = get_products()
    return render_template('home.html', products=products)

@app.route('/home')
def home():
    products = get_products()
    return render_template('home.html', products=products)

@app.route('/san-pham/<category>')
def products_by_category(category):
    products = get_products_by_category(category)
    return render_template('home.html', products=products, current_category=category)

@app.route('/chitietsanpham/<int:product_id>')
def chitietsanpham(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Sản phẩm không tồn tại!', 'error')
        return redirect(url_for('home'))
    return render_template('chitietsanpham.html', product=product)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/submit', methods=['POST'])
def login_submit():
    username = request.form.get('username')
    password = request.form.get('password')
    # Xử lý đăng nhập đơn giản (cần kết nối DB thật)
    if username and password:
        flash(f'Đăng nhập thành công! Chào mừng {username}', 'success')
        return redirect(url_for('home'))
    else:
        flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')
        return redirect(url_for('login'))

@app.route('/register')
def register():
    return render_template('dangky.html')

@app.route('/register/submit', methods=['POST'])
def register_submit():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    if fullname and email and phone and password and confirm_password:
        if password == confirm_password:
            flash(f'Đăng ký thành công! Chào mừng {fullname} đến với ShoeStore!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Mật khẩu xác nhận không khớp!', 'error')
            return redirect(url_for('register'))
    else:
        flash('Vui lòng điền đầy đủ thông tin!', 'error')
        return redirect(url_for('register'))

@app.route('/logout')
def logout():
    flash('Đã đăng xuất thành công!', 'success')
    return redirect(url_for('home'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/contact/submit', methods=['POST'])
def contact_submit():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    subject = request.form.get('subject')
    message = request.form.get('message')
    flash(f'Cảm ơn {first_name} {last_name}! Chúng tôi đã nhận được tin nhắn của bạn.', 'success')
    return redirect(url_for('contact'))

# ================== GIỎ HÀNG ĐƠN GIẢN (session) ==================
def get_cart_items():
    return session.get("cart", [])

def get_cart_count():
    return sum(item["quantity"] for item in session.get("cart", []))

@app.route('/giohang')
def giohang():
    cart_items = get_cart_items()
    return render_template('giohang.html', cart_items=cart_items, cart_count=get_cart_count())

@app.route('/add_to_giohang', methods=['POST'])
def add_to_giohang():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    product = get_product_by_id(product_id)
    if not product:
        flash('Sản phẩm không tồn tại!', 'error')
        return redirect(url_for('home'))
    if "cart" not in session:
        session["cart"] = []
    cart = session["cart"]
    for item in cart:
        if item["product_id"] == int(product_id):
            item["quantity"] += quantity
            session["cart"] = cart
            flash(f'Đã thêm "{product["name"]}" vào giỏ hàng!', 'success')
            return redirect(url_for('giohang'))
    cart.append({
        "product_id": int(product_id),
        "name": product["name"],
        "price": product["price"],
        "quantity": quantity,
        "image": product.get("image", "")
    })
    session["cart"] = cart
    flash(f'Đã thêm "{product["name"]}" vào giỏ hàng!', 'success')
    return redirect(url_for('giohang'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = int(request.form.get('product_id'))
    if "cart" in session:
        cart = session["cart"]
        cart = [item for item in cart if item["product_id"] != product_id]
        session["cart"] = cart
        flash('Đã xóa sản phẩm khỏi giỏ hàng!', 'success')
    return redirect(url_for('giohang'))

@app.route('/clear_cart')
def clear_cart():
    session["cart"] = []
    flash('Đã xóa toàn bộ giỏ hàng!', 'success')
    return redirect(url_for('giohang'))

if __name__ == '__main__':
    app.run(debug=True)