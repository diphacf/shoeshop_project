from flask import Flask, render_template, session, flash, redirect, url_for, request, jsonify
from flask_cors import CORS
from routes.product_routes import product_bp
from routes.user_routes import user_bp
from routes.order_routes import order_bp
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = 'your_secret_key'
CORS(app)

# Đăng ký các blueprint
app.register_blueprint(product_bp, url_prefix="/api/products")
app.register_blueprint(user_bp, url_prefix="/api/users")
app.register_blueprint(order_bp, url_prefix="/api/orders")

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
    cursor.execute("SELECT * FROM products WHERE category_id=%s", (category,))
    products = cursor.fetchall()
    cursor.close()
    return products

@app.route('/')
def index():
    category_id = request.args.get('category_id')

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Lấy danh sách category để hiển thị dropdown
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    if category_id:
        products = get_products_by_category(category_id)
    else:
        products = get_products()

    cursor.close()
    conn.close()

    return render_template("home.html", 
                           categories=categories, 
                           products=products, 
                           current_category=category_id)

@app.route('/home')
def home():
    category_id = request.args.get('category_id')

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Lấy danh sách category để hiển thị dropdown
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    if category_id:
        products = get_products_by_category(category_id)
    else:
        products = get_products()

    cursor.close()
    conn.close()

    return render_template("home.html", 
                           categories=categories, 
                           products=products, 
                           current_category=category_id)

@app.route('/products/category/<string:category_name>')
def products_by_category(category_name):
    products = get_products_by_category(category_name)

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("home.html",
                           categories=categories,
                           products=products,
                           current_category=category_name)

@app.route('/chitietsanpham/<int:product_id>')
def chitietsanpham(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash('Sản phẩm không tồn tại!', 'error')
        return redirect(url_for('home'))
    return render_template('chitietsanpham.html', product=product)

@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if q:
        cursor.execute("SELECT * FROM products WHERE name LIKE %s OR description LIKE %s", (f"%{q}%", f"%{q}%"))
        products = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
    cursor.close()
    return render_template('home.html', products=products, search_query=q)

@app.route('/dangky')
def dangky():
    return render_template('dangky.html')

@app.route('/dangky/submit', methods=['POST'])
def dangky_submit():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    if password != confirm_password:
        flash('Mật khẩu xác nhận không khớp!', 'error')
        return redirect(url_for('dangky'))
    
    if fullname and email and password:
        try:
            conn = get_db()
            cursor = conn.cursor()

            # kiểm tra email trùng lặp
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('Email đã được sử dụng!', 'error')
                return redirect(url_for('dangky'))

            hashed_pw = generate_password_hash(password)

            cursor.execute(
                "INSERT INTO users (full_name, email, password_hash) VALUES (%s, %s, %s)",
                (fullname, email, hashed_pw)
            )

            conn.commit()
            cursor.close()
            conn.close()

            return jsonify({"success": True, "message": "Đăng ký thành công!"})
        except Exception as e:
            return jsonify({"success": False, "message": f"Lỗi: {str(e)}"})
    else:
        flash('Vui lòng điền đầy đủ thông tin!', 'error')
        return redirect(url_for('dangky'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/submit', methods=['POST'])
def login_submit():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    
    if not email or not password:
        flash('Vui lòng nhập đầy đủ thông tin!', 'error')
        return redirect(url_for('login'))
    
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s LIMIT 1", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session['user_id'] = user['user_id']
            session['user_name'] = user['full_name']
            return jsonify(success=True, message=f"Đăng nhập thành công! Chào mừng {user['full_name']}")
        else:
            return jsonify(success=False, message="Tên đăng nhập hoặc mật khẩu không đúng!")

    except Exception as e:
        return jsonify(success=False, message=f"Lỗi hệ thống: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/logout')
def logout():
    session.clear()  # xóa tất cả thông tin đăng nhập
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

def get_image_path(product):
    # 1) Prefer the computed local image name (img_local)
    fname = product.get('img_local')
    if fname:
        local_path = os.path.join(str(app.root_path), 'static', 'images', fname)
        if os.path.isfile(local_path):
            # cache-busting bằng mtime để trình duyệt tải lại khi bạn thay ảnh
            try:
                mtime = int(os.path.getmtime(local_path))
            except Exception:
                mtime = 0
            return url_for('static', filename=f'images/{fname}', v=mtime)

    # 2) If product['img'] is a local filename (not http or absolute), check it too
    img_field = product.get('img') or ''
    if isinstance(img_field, str) and not img_field.startswith('http') and not img_field.startswith('/'):
        local_path2 = os.path.join(str(app.root_path), 'static', 'images', img_field)
        if os.path.isfile(local_path2):
            try:
                mtime = int(os.path.getmtime(local_path2))
            except Exception:
                mtime = 0
            return url_for('static', filename=f'images/{img_field}', v=mtime)

    # Fallback to the original value (could be external URL)
    return product.get('img')

app.jinja_env.globals['get_image_path'] = get_image_path

if __name__ == '__main__':
    app.run(debug=True)