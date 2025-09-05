from flask import Flask, flash, redirect, render_template, url_for, request, session
import unicodedata
import os
import json
from functools import wraps
from admin_config import DEFAULT_ADMIN_CREDENTIALS, ADMIN_SESSION_TIMEOUT
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Admin credentials (sử dụng từ config file)
ADMIN_CREDENTIALS = DEFAULT_ADMIN_CREDENTIALS

# ==== SIMPLE USER STORAGE (JSON FILE) ====
USERS_FILE = os.path.join(str(os.path.dirname(__file__)), 'users.json')

def _ensure_users_file_exists():
    if not os.path.isfile(USERS_FILE):
        try:
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False)
            print('[INFO] Created users.json')
        except Exception as e:
            print(f'[ERROR] Cannot create users.json: {e}')

def _load_users():
    if not os.path.isfile(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        return []

def _save_users(users):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        print(f'[INFO] Saved {len(users)} users to users.json')
    except Exception as e:
        print(f'[ERROR] Failed to save users.json: {e}')

def _find_user_by_email(email):
    email_norm = (email or '').strip().lower()
    for u in _load_users():
        if u.get('email', '').lower() == email_norm:
            return u
    return None

def admin_required(f):
    """Decorator để yêu cầu đăng nhập admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session or not session['admin_logged_in']:
            flash('Vui lòng đăng nhập để truy cập trang admin!', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def check_admin_session():
    """Kiểm tra session admin có hợp lệ không"""
    admin_routes = ['admin', 'admin_get_product', 'admin_add_product', 'admin_edit_product', 'admin_delete_product', 'admin_v2']
    
    if request.endpoint in admin_routes:
        if 'admin_logged_in' not in session or not session.get('admin_logged_in'):
            if request.endpoint != 'admin_login':
                return redirect(url_for('admin_login'))
    
    # Auto logout sau 2 giờ không hoạt động (tùy chọn)
    # if 'admin_logged_in' in session and 'admin_last_activity' in session:
    #     from datetime import datetime, timedelta
    #     last_activity = datetime.fromisoformat(session['admin_last_activity'])
    #     if datetime.now() - last_activity > timedelta(hours=2):
    #         session.pop('admin_logged_in', None)
    #         session.pop('admin_username', None)
    #         session.pop('admin_last_activity', None)
    #         flash('Phiên đăng nhập đã hết hạn!', 'error')
    #         return redirect(url_for('admin_login'))

# Danh sách sản phẩm chung
PRODUCTS = [
    {
        'id': 0,
        'name': 'Dép Sandal Đỏ Trắt',
        'price': '800.000 đ',
        'price_num': 800000,
        'desc': 'Dép sandal nữ đi chơi đi học thoáng tích cực',
        'img': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80',
        'sizes': [35, 36, 37, 38, 39, 40, 41, 42],
        'category': 'dép',
        'rating': 5,
        'tag': 'Sale'
    },
    {
        'id': 1,
        'name': 'Dép Sục Nữ',
        'price': '650.000 đ',
        'price_num': 650000,
        'desc': 'Dép sục nữ đi trong nhà thời trang hiện đại',
        'img': 'https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80',
        'sizes': [35, 36, 37, 38, 39, 40, 41],
        'category': 'dép',
        'rating': 5,
        'tag': 'Hot'
    },
    {
        'id': 2,
        'name': 'Dép Tông Cao Su',
        'price': '300.000 đ',
        'price_num': 300000,
        'desc': 'Dép cao su đi chơi đi biển thoáng mát',
        'img': 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80',
        'sizes': [36, 37, 38, 39, 40, 41, 42],
        'category': 'dép',
        'rating': 4,
        'tag': None
    },
    {
        'id': 3,
        'name': 'Giày Boot Cổ Cao',
        'price': '2.200.000 đ',
        'price_num': 2200000,
        'desc': 'Bộ giày nữ cổ cao thời trang phong cách',
        'img': 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80',
        'sizes': [35, 36, 37, 38, 39, 40, 41, 42],
        'category': 'giày',
        'rating': 5,
        'tag': None
    },
    {
        'id': 4,
        'name': 'Giày Cao Gót Nữ',
        'price': '1.800.000 đ',
        'price_num': 1800000,
        'desc': 'Giày cao gót thiết kế sang trọng, thanh lịch',
        'img': 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80',
        'sizes': [35, 36, 37, 38, 39, 40, 41],
        'category': 'giày',
        'rating': 4,
        'tag': 'New'
    },
    {
        'id': 5,
        'name': 'Giày Oxford Nam',
        'price': '2.500.000 đ',
        'price_num': 2500000,
        'desc': 'Giày da thật cao cấp dành cho doanh nhân',
        'img': 'https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80',
        'sizes': [38, 39, 40, 41, 42, 43, 44],
        'category': 'giày',
        'rating': 5,
        'tag': None
    },
    {
        'id': 6,
        'name': 'Giày Sneaker Premium',
        'price': '1.500.000 đ',
        'price_num': 1500000,
        'desc': 'Giày thể thao cao cấp với chất liệu đỉnh cao',
        'img': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80',
        'sizes': [36, 37, 38, 39, 40, 41, 42, 43],
        'category': 'giày',
        'rating': 5,
        'tag': 'Sale'
    },
    {
        'id': 7,
        'name': 'Giày Thể Thao Nam',
        'price': '1.200.000 đ',
        'price_num': 1200000,
        'desc': 'Giày chạy bộ công nghệ mới, thoải mái nhất',
        'img': 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&q=80',
        'sizes': [38, 39, 40, 41, 42, 43, 44, 45],
        'category': 'giày',
        'rating': 4,
        'tag': 'Best'
    },
    # ==== Shondo additions (cập nhật hình phù hợp) ====
    {
        'id': 8,
        'name': 'Sandal Shondo Urban Đen',
        'price': '780.000 đ',
        'price_num': 780000,
        'desc': 'Sandal Shondo đế êm, bám tốt phù hợp đi phố & du lịch',
        'img': 'https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?auto=format&fit=crop&w=400&q=80',
        'sizes': [37, 38, 39, 40, 41, 42, 43],
        'category': 'dép',
        'rating': 5,
        'tag': 'New'
    },
    {
        'id': 9,
        'name': 'Sandal Shondo Outdoor Xám',
        'price': '820.000 đ',
        'price_num': 820000,
        'desc': 'Thiết kế chắc chắn, quai sợi chịu lực – Shondo trekking',
        'img': 'https://images.unsplash.com/photo-1600185365584-c9e381730637?auto=format&fit=crop&w=400&q=80',
        'sizes': [38, 39, 40, 41, 42, 43, 44],
        'category': 'dép',
        'rating': 4,
        'tag': 'Sale'
    },
    {
        'id': 10,
        'name': 'Sandal Shondo Limited Trắng',
        'price': '890.000 đ',
        'price_num': 890000,
        'desc': 'Phiên bản giới hạn phối màu trắng tối giản cao cấp',
        'img': 'https://images.unsplash.com/photo-1600185365973-26e776d1252d?auto=format&fit=crop&w=400&q=80',
        'sizes': [36, 37, 38, 39, 40, 41],
        'category': 'dép',
        'rating': 5,
        'tag': 'Hot'
    },
    {
        'id': 11,
        'name': 'Giày Shondo Sneaker Active',
        'price': '1.150.000 đ',
        'price_num': 1150000,
        'desc': 'Sneaker Shondo nhẹ, lót thoáng khí dành cho hoạt động hàng ngày',
        'img': 'https://images.unsplash.com/photo-1600185365207-c7bf225d2b4f?auto=format&fit=crop&w=400&q=80',
        'sizes': [37, 38, 39, 40, 41, 42, 43],
        'category': 'giày',
        'rating': 5,
        'tag': None
    },
    {
        'id': 12,
        'name': 'Giày Shondo Street Chunky',
        'price': '1.350.000 đ',
        'price_num': 1350000,
        'desc': 'Phong cách đế dày thời trang, hỗ trợ nâng đỡ bàn chân',
        'img': 'https://images.unsplash.com/photo-1600185365065-52e160b48a25?auto=format&fit=crop&w=400&q=80',
        'sizes': [36, 37, 38, 39, 40, 41, 42],
        'category': 'giày',
        'rating': 4,
        'tag': 'New'
    },
    {
        'id': 13,
        'name': 'Giày Shondo Performance Run',
        'price': '1.480.000 đ',
        'price_num': 1480000,
        'desc': 'Đệm phản hồi năng lượng, phù hợp chạy bộ đường dài',
        'img': 'https://images.unsplash.com/photo-1600185365730-36e8e4c9ba06?auto=format&fit=crop&w=400&q=80',
        'sizes': [39, 40, 41, 42, 43, 44],
        'category': 'giày',
        'rating': 5,
        'tag': 'Best'
    },
    {
        'id': 14,
        'name': 'Sandal Shondo Travel Navy',
        'price': '760.000 đ',
        'price_num': 760000,
        'desc': 'Êm ái, chống trượt tốt – đồng hành mọi chuyến đi',
        'img': 'https://images.unsplash.com/photo-1600185365174-5e9b717f2c68?auto=format&fit=crop&w=400&q=80',
        'sizes': [37, 38, 39, 40, 41, 42],
        'category': 'dép',
        'rating': 4,
        'tag': None
    },
    {
        'id': 15,
        'name': 'Sandal Shondo Kids Color',
        'price': '520.000 đ',
        'price_num': 520000,
        'desc': 'Dòng trẻ em nhẹ, quai dán dễ chỉnh, màu sắc vui nhộn',
        'img': 'https://images.unsplash.com/photo-1600185365397-c89c8e1cc7ec?auto=format&fit=crop&w=400&q=80',
        'sizes': [30, 31, 32, 33, 34, 35, 36],
        'category': 'dép',
        'rating': 5,
        'tag': 'Sale'
    },
    {
        'id': 16,
        'name': 'Giày Shondo Minimal Grey',
        'price': '1.050.000 đ',
        'price_num': 1050000,
        'desc': 'Thiết kế tối giản, phối màu trung tính dễ phối đồ',
        'img': 'https://images.unsplash.com/photo-1600185366296-8e6db7bf784d?auto=format&fit=crop&w=400&q=80',
        'sizes': [37, 38, 39, 40, 41, 42],
        'category': 'giày',
        'rating': 4,
        'tag': None
    }
]

# ==== TẠO TÊN FILE ẢNH LOCAL (LOẠI BỎ TIỀN TỐ LẶP) ====
STOP_PREFIXES = { 'giay', 'dep', 'sandal', 'shondo', 'giày', 'dép' }

def _normalize_basic(text: str) -> str:
    nfkd = unicodedata.normalize('NFD', text)
    no_diac = ''.join(ch for ch in nfkd if not unicodedata.combining(ch))
    cleaned = ''.join(ch.lower() if ch.isalnum() else ' ' for ch in no_diac)
    return ' '.join(cleaned.split())

def _build_slug(name: str) -> str:
    base = _normalize_basic(name)
    tokens = base.split()
    # Bỏ lần lượt các token đầu nếu nằm trong STOP_PREFIXES
    while tokens and tokens[0] in STOP_PREFIXES:
        tokens.pop(0)
    if not tokens:  # fallback nếu xoá hết
        tokens = base.split()
    return '-'.join(tokens)

def _assign_local_image_names():
    for p in PRODUCTS:
        prefix = 'giay' if p.get('category') == 'giày' else 'dep'
        core = _build_slug(p.get('name',''))
        p['img_local'] = f"{prefix}-{core}.jpg"

_assign_local_image_names()

# Manual overrides for specific products where the automatic slug doesn't match the stored filenames
# e.g. 'Dép Sandal Đỏ Trắt' should map to the existing file 'dep-sandal-do-trat.jpg'
for p in PRODUCTS:
    if p.get('name') == 'Dép Sandal Đỏ Trắt':
        p['img_local'] = 'dep-sandal-do-trat.jpg'

# ==== IMAGE RESOLUTION (no lru_cache, always re-check existence) ====
# Gỡ bỏ @lru_cache để thay đổi file hệ thống được nhận ngay

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

# Route debug để kiểm tra file local đã được nhận chưa
@app.route('/debug-images')
def debug_images():
    rows = []
    for p in PRODUCTS:
        fname = p.get('img_local')
        local_path = os.path.join(str(app.root_path), 'static', 'images', fname)
        exists = os.path.isfile(local_path)
        rows.append({ 'id': p['id'], 'name': p['name'], 'img_local': fname, 'exists': exists })

    return {'images': rows, 'static_dir': os.path.join(str(app.root_path), 'static', 'images')}

def get_product_by_id(product_id):
    """Lấy sản phẩm theo ID"""
    for product in PRODUCTS:
        if product['id'] == int(product_id):
            return product
    return None

# Expose helper to templates so cart can resolve full product objects
app.jinja_env.globals['get_product_by_id'] = get_product_by_id

def get_cart_items():
    """Lấy danh sách sản phẩm trong giỏ hàng"""
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']

def add_to_cart(product_id, size=None, quantity=1):
    """Thêm sản phẩm vào giỏ hàng"""
    cart = get_cart_items()
    product = get_product_by_id(product_id)
    
    if not product:
        return False
    
    # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa (cùng size)
    for item in cart:
        if item['product_id'] == int(product_id) and item.get('size') == size:
            item['quantity'] += int(quantity)
            session['cart'] = cart
            return True
    
    # Thêm sản phẩm mới vào giỏ hàng
    cart_item = {
        'product_id': int(product_id),
        'name': product['name'],
        'price': product['price'],
        'price_num': product['price_num'],
    'img': get_image_path(product),
        'size': size,
        'quantity': int(quantity)
    }
    
    cart.append(cart_item)
    session['cart'] = cart
    return True

def get_cart_total():
    """Tính tổng tiền trong giỏ hàng"""
    cart = get_cart_items()
    total = 0
    for item in cart:
        total += item['price_num'] * item['quantity']
    return total

def calculate_final_total():
    """Tính tổng tiền cuối cùng sau khi áp dụng promo và phí ship"""
    cart_total = get_cart_total()
    
    # Calculate shipping fee (free for orders over 1,000,000 VND)
    shipping_fee = 0 if cart_total >= 1000000 else 30000
    
    # Calculate promo discount
    promo_discount = 0
    if 'applied_promo' in session:
        promo = session['applied_promo']
        if promo.get('discount', 0) > 0:
            promo_discount = cart_total * promo['discount']
        if promo.get('free_ship', False):
            shipping_fee = 0
    
    final_total = cart_total + shipping_fee - promo_discount
    
    return {
        'cart_total': cart_total,
        'shipping_fee': shipping_fee,
        'promo_discount': promo_discount,
        'final_total': final_total
    }

def get_cart_count():
    """Đếm số lượng sản phẩm trong giỏ hàng"""
    cart = get_cart_items()
    count = 0
    for item in cart:
        count += item['quantity']
    return count 
@app.route('/')
def index():
    return render_template('home.html', products=PRODUCTS, cart_count=get_cart_count())

@app.route('/home')
def home():
    return render_template('home.html', products=PRODUCTS, cart_count=get_cart_count())

@app.route('/dangky')
def dangky():
    return redirect(url_for('register'))

@app.route('/dangky/submit', methods=['POST'])
def dangky_submit():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    # Xử lý đăng ký đơn giản
    if password != confirm_password:
        flash('Mật khẩu xác nhận không khớp!', 'error')
        return redirect(url_for('dangky'))
    
    if username and email and password:
        flash(f'Đăng ký thành công! Chào mừng {username}', 'success')
        return redirect(url_for('login'))
    else:
        flash('Vui lòng điền đầy đủ thông tin!', 'error')
        return redirect(url_for('dangky'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/submit', methods=['POST'])
def login_submit():
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Kiểm tra nếu là admin đăng nhập
    if email in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[email] == password:
        session['admin_logged_in'] = True
        session['admin_username'] = email
        flash(f'Chào mừng Admin {email}! Đăng nhập thành công.', 'success')
        return redirect(url_for('admin'))
    
    # Xử lý đăng nhập khách hàng thường (dùng JSON lưu trữ cục bộ)
    if email and password:
        user = _find_user_by_email(email)
        if user and check_password_hash(user.get('password_hash', ''), password):
            session['user_logged_in'] = True
            session['user_email'] = user['email']
            session['user_fullname'] = user.get('fullname')
            flash(f'Đăng nhập thành công! Chào mừng {user.get("fullname") or email}', 'success')
            return redirect(url_for('home'))
        else:
            flash('Email hoặc mật khẩu không đúng!', 'error')
            return redirect(url_for('login'))
    else:
        flash('Email hoặc mật khẩu không đúng!', 'error')
        return redirect(url_for('login'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register/submit', methods=['POST'])
def register_submit():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    
    # Xử lý đăng ký với lưu trữ JSON + hash mật khẩu
    if not (fullname and email and phone and password and confirm_password):
        flash('Vui lòng điền đầy đủ thông tin!', 'error')
        return redirect(url_for('register'))

    if password != confirm_password:
        flash('Mật khẩu xác nhận không khớp!', 'error')
        return redirect(url_for('register'))

    # Lưu vào file JSON cục bộ
    if _find_user_by_email(email):
        flash('Email đã được sử dụng!', 'error')
        return redirect(url_for('register'))

    _ensure_users_file_exists()
    users = _load_users()
    users.append({
        'fullname': fullname.strip(),
        'email': email.strip().lower(),
        'phone': phone.strip(),
        'password_hash': generate_password_hash(password)
    })
    _save_users(users)

    flash(f'Đăng ký thành công! Chào mừng {fullname} đến với ShoeStore!', 'success')
    return redirect(url_for('login'))

#

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

@app.route('/apply_promo', methods=['POST'])
def apply_promo():
    """Áp dụng mã giảm giá"""
    promo_code = request.form.get('promo_code', '').strip().upper()
    
    # Định nghĩa các mã giảm giá
    promo_codes = {
        'WELCOME10': {'discount': 0.1, 'min_order': 500000, 'description': 'Giảm 10% cho đơn hàng từ 500,000đ'},
        'SUMMER20': {'discount': 0.2, 'min_order': 1000000, 'description': 'Giảm 20% cho đơn hàng từ 1,000,000đ'},
        'FREESHIP': {'discount': 0, 'free_ship': True, 'min_order': 300000, 'description': 'Miễn phí vận chuyển cho đơn hàng từ 300,000đ'}
    }
    
    cart_total = get_cart_total()
    
    if promo_code in promo_codes:
        promo = promo_codes[promo_code]
        if cart_total >= promo['min_order']:
            # Store promo in session
            session['applied_promo'] = {
                'code': promo_code,
                'discount': promo.get('discount', 0),
                'free_ship': promo.get('free_ship', False),
                'description': promo['description']
            }
            flash(f'Đã áp dụng mã giảm giá "{promo_code}"! {promo["description"]}', 'success')
        else:
            flash(f'Mã giảm giá "{promo_code}" yêu cầu đơn hàng tối thiểu {promo["min_order"]:,}đ', 'error')
    else:
        flash('Mã giảm giá không hợp lệ!', 'error')
    
    return redirect(url_for('giohang'))

@app.route('/remove_promo')
def remove_promo():
    """Xóa mã giảm giá"""
    if 'applied_promo' in session:
        del session['applied_promo']
        flash('Đã xóa mã giảm giá!', 'success')
    return redirect(url_for('giohang'))

@app.route('/products')
def products():
    return render_template('home.html', products=PRODUCTS, cart_count=get_cart_count())

@app.route('/logout')
def logout():
    session.pop('user_logged_in', None)
    session.pop('user_email', None)
    session.pop('user_fullname', None)
    flash('Đã đăng xuất thành công!', 'success')
    return redirect(url_for('home'))

@app.route('/chitietsanpham/<int:id>')
def chitietsanpham(id):
    product = get_product_by_id(id)
    if not product:
        flash('Sản phẩm không tồn tại!', 'error')
        return redirect(url_for('home'))
    
    return render_template('chitietsanpham.html', product=product, cart_count=get_cart_count())

@app.route('/admin')
@admin_required
def admin():
    return render_template('admin.html', products=PRODUCTS)

@app.route('/admin/login')
def admin_login():
    # Nếu đã đăng nhập, redirect to admin
    if 'admin_logged_in' in session and session['admin_logged_in']:
        return redirect(url_for('admin'))
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    # Kiểm tra thông tin đăng nhập
    if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
        session['admin_logged_in'] = True
        session['admin_username'] = username
        flash(f'Chào mừng {username}! Đăng nhập thành công.', 'success')
        return redirect(url_for('admin'))
    else:
        flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Đã đăng xuất thành công!', 'success')
    return redirect(url_for('home'))

@app.route('/admin/v2')
@admin_required
def admin_v2():
    return render_template('admin_v2.html', products=PRODUCTS)

@app.route('/admin/get_product/<int:product_id>')
@admin_required
def admin_get_product(product_id):
    """Lấy thông tin sản phẩm theo ID cho chức năng edit"""
    product = get_product_by_id(product_id)
    if not product:
        return {'error': 'Product not found'}, 404
    return product

@app.route('/admin/add_product', methods=['POST'])
@admin_required
def admin_add_product():
    """Thêm sản phẩm mới"""
    try:
        # Lấy dữ liệu từ form
        name = request.form.get('name')
        if not name or not name.strip():
            flash('Tên sản phẩm không được để trống!', 'error')
            return redirect(url_for('admin'))
            
        price_num_str = request.form.get('price_num')
        if not price_num_str:
            flash('Giá sản phẩm không được để trống!', 'error')
            return redirect(url_for('admin'))
        price_num = int(price_num_str)
        
        category = request.form.get('category')
        if not category:
            flash('Danh mục không được để trống!', 'error')
            return redirect(url_for('admin'))
            
        tag = request.form.get('tag') if request.form.get('tag') else None
        desc = request.form.get('desc', '')
        rating_str = request.form.get('rating', '5')
        rating = int(rating_str) if rating_str else 5
        sizes_str = request.form.get('sizes', '')
        
        # Xử lý sizes
        sizes = []
        if sizes_str:
            try:
                sizes = [int(size.strip()) for size in sizes_str.split(',') if size.strip()]
            except ValueError:
                flash('Kích thước phải là các số nguyên cách nhau bởi dấu phẩy!', 'error')
                return redirect(url_for('admin'))
        
        # Tạo ID mới
        new_id = max([p['id'] for p in PRODUCTS]) + 1 if PRODUCTS else 0
        
        # Handle image selection (local image file)
        image_url = "https://images.unsplash.com/photo-1549298916-b41d501d3772?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80"  # default
        image_file = request.form.get('image_file')
        if image_file and image_file != '':
            # Use local image from static/images folder
            image_url = f'/static/images/{image_file}'
        
        # Handle file upload if provided (fallback for manual uploads)
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and file.filename != '':
                # In a real application, you would save the file and get its URL
                # For now, we'll use the local image if provided, otherwise placeholder
                pass
        
        # Tạo sản phẩm mới
        new_product = {
            'id': new_id,
            'name': name.strip(),
            'price': f'{price_num:,} đ'.replace(',', '.'),
            'price_num': price_num,
            'desc': desc.strip(),
            'img': image_url,
            'sizes': sizes,
            'category': category,
            'rating': rating,
            'tag': tag
        }
        
        # Thêm vào danh sách
        PRODUCTS.append(new_product)
        
        # Tạo lại tên file ảnh local
        _assign_local_image_names()
        
        flash(f'Đã thêm sản phẩm "{name}" thành công!', 'success')
        
    except ValueError as ve:
        flash(f'Dữ liệu không hợp lệ: {str(ve)}', 'error')
    except Exception as e:
        flash(f'Lỗi khi thêm sản phẩm: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/edit_product/<int:product_id>', methods=['POST'])
@admin_required
def admin_edit_product(product_id):
    """Chỉnh sửa sản phẩm"""
    try:
        # Tìm sản phẩm
        product = get_product_by_id(product_id)
        if not product:
            flash('Sản phẩm không tồn tại!', 'error')
            return redirect(url_for('admin'))
        
        # Lấy dữ liệu từ form
        name = request.form.get('name')
        if not name or not name.strip():
            flash('Tên sản phẩm không được để trống!', 'error')
            return redirect(url_for('admin'))
        
        price_num_str = request.form.get('price_num')
        if not price_num_str:
            flash('Giá sản phẩm không được để trống!', 'error')
            return redirect(url_for('admin'))
        price_num = int(price_num_str)
        
        category = request.form.get('category')
        if not category:
            flash('Danh mục không được để trống!', 'error')
            return redirect(url_for('admin'))
        
        # Cập nhật thông tin
        old_name = product['name']
        product['name'] = name.strip()
        product['price_num'] = price_num
        product['price'] = f'{price_num:,} đ'.replace(',', '.')
        product['category'] = category
        product['tag'] = request.form.get('tag') if request.form.get('tag') else None
        product['desc'] = request.form.get('desc', '').strip()
        rating_str = request.form.get('rating', '5')
        product['rating'] = int(rating_str) if rating_str else 5
        
        # Xử lý sizes
        sizes_str = request.form.get('sizes', '')
        if sizes_str:
            try:
                product['sizes'] = [int(size.strip()) for size in sizes_str.split(',') if size.strip()]
            except ValueError:
                flash('Kích thước phải là các số nguyên cách nhau bởi dấu phẩy!', 'error')
                return redirect(url_for('admin'))
        else:
            product['sizes'] = []
        
        # Handle image selection (local image file)
        image_file = request.form.get('image_file')
        if image_file and image_file != '':
            # Use local image from static/images folder
            product['img'] = f'/static/images/{image_file}'
        
        # Handle file upload if provided (fallback for manual uploads)
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and file.filename != '':
                # In a real application, you would save the file and update the image URL
                # For now, we'll keep the existing image
                pass
        
        # Tạo lại tên file ảnh local
        _assign_local_image_names()
        
        flash(f'Đã cập nhật sản phẩm "{product["name"]}" thành công!', 'success')
        
    except ValueError as ve:
        flash(f'Dữ liệu không hợp lệ: {str(ve)}', 'error')
    except Exception as e:
        flash(f'Lỗi khi cập nhật sản phẩm: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/delete_product/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    """Xóa sản phẩm"""
    try:
        # Tìm và xóa sản phẩm
        product = get_product_by_id(product_id)
        if not product:
            flash('Sản phẩm không tồn tại!', 'error')
            return redirect(url_for('admin'))
        
        product_name = product['name']
        
        # Xóa khỏi danh sách
        global PRODUCTS
        PRODUCTS = [p for p in PRODUCTS if p['id'] != product_id]
        
        flash(f'Đã xóa sản phẩm "{product_name}" thành công!', 'success')
        
    except Exception as e:
        flash(f'Lỗi khi xóa sản phẩm: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/contact')
def contact():
    return render_template('contact.html', cart_count=get_cart_count())

@app.route('/contact/submit', methods=['POST'])
def contact_submit():
    # Lấy dữ liệu từ form
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    subject = request.form.get('subject')
    message = request.form.get('message')
    
    # Xử lý dữ liệu (tạm thời chỉ flash message)
    flash(f'Cảm ơn {first_name} {last_name}! Chúng tôi đã nhận được tin nhắn của bạn và sẽ phản hồi sớm nhất có thể.', 'success')
    return redirect(url_for('contact'))

@app.route('/add_to_giohang', methods=['POST'])
def add_to_giohang():
    # Lấy dữ liệu từ form
    product_id = request.form.get('product_id')
    size = request.form.get('size')
    quantity_str = request.form.get('quantity', '1')
    
    if not product_id:
        flash('Có lỗi xảy ra khi thêm sản phẩm vào giỏ hàng!', 'error')
        return redirect(url_for('home'))
    
    try:
        quantity = int(quantity_str) if quantity_str else 1
    except ValueError:
        quantity = 1
    
    # Lấy thông tin sản phẩm
    product = get_product_by_id(product_id)
    if not product:
        flash('Sản phẩm không tồn tại!', 'error')
        return redirect(url_for('home'))
    
    # Thêm vào giỏ hàng
    if add_to_cart(product_id, size, quantity):
        flash(f'Đã thêm "{product["name"]}" vào giỏ hàng!', 'success')
    else:
        flash('Có lỗi xảy ra khi thêm sản phẩm vào giỏ hàng!', 'error')
    
    # Redirect về trang trước đó hoặc trang chủ
    return redirect(request.referrer or url_for('home'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    """Xóa sản phẩm khỏi giỏ hàng"""
    product_id_str = request.form.get('product_id')
    size = request.form.get('size')
    
    if not product_id_str:
        flash('Có lỗi xảy ra!', 'error')
        return redirect(url_for('giohang'))
    
    try:
        product_id = int(product_id_str)
    except ValueError:
        flash('ID sản phẩm không hợp lệ!', 'error')
        return redirect(url_for('giohang'))
    
    if 'cart' in session:
        cart = session['cart']
        # Tìm và xóa sản phẩm khỏi giỏ hàng
        cart = [item for item in cart if not (item['product_id'] == product_id and item.get('size') == size)]
        session['cart'] = cart
        flash('Đã xóa sản phẩm khỏi giỏ hàng!', 'success')
    
    return redirect(url_for('giohang'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    """Cập nhật số lượng sản phẩm trong giỏ hàng"""
    product_id_str = request.form.get('product_id')
    size = request.form.get('size')
    quantity_str = request.form.get('quantity')
    
    if not product_id_str or not quantity_str:
        flash('Dữ liệu không hợp lệ!', 'error')
        return redirect(url_for('giohang'))
    
    try:
        product_id = int(product_id_str)
        quantity = int(quantity_str)
    except ValueError:
        flash('Dữ liệu không hợp lệ!', 'error')
        return redirect(url_for('giohang'))
    
    if 'cart' in session and quantity > 0:
        cart = session['cart']
        for item in cart:
            if item['product_id'] == product_id and item.get('size') == size:
                item['quantity'] = quantity
                break
        session['cart'] = cart
        flash('Đã cập nhật giỏ hàng!', 'success')
    elif quantity <= 0:
        # Xóa sản phẩm nếu số lượng <= 0
        return remove_from_cart()
    
    return redirect(url_for('giohang'))

@app.route('/clear_cart')
def clear_cart():
    """Xóa toàn bộ giỏ hàng"""
    session['cart'] = []
    # Also clear any applied promo codes
    if 'applied_promo' in session:
        del session['applied_promo']
    flash('Đã xóa toàn bộ giỏ hàng!', 'success')
    return redirect(url_for('giohang'))

@app.route('/san-pham/<category>')
def products_by_category(category):
    raw = category.lower()
    mapping = { 'giay':'giày', 'giày':'giày', 'dep':'dép', 'dép':'dép' }
    cat = mapping.get(raw, raw)
    filtered = [p for p in PRODUCTS if p['category'] == cat]
    if not filtered:  # nếu không có khớp thì quay về tất cả
        filtered = PRODUCTS
        raw = None
        cat = None
    return render_template('home.html', products=filtered, cart_count=get_cart_count(), current_category=raw, display_category=cat)

# ====== SEARCH FEATURE ======

def normalize_text(s: str) -> str:
    """Chuẩn hoá chuỗi bỏ dấu để tìm kiếm không phân biệt dấu."""
    if not s:
        return ''
    nfkd = unicodedata.normalize('NFD', s)
    return ''.join(ch for ch in nfkd if not unicodedata.combining(ch)).lower()

@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    results = []
    if q:
        nq = normalize_text(q)
        for p in PRODUCTS:
            if nq in normalize_text(p['name']) or nq in normalize_text(p['desc']):
                results.append(p)
    else:
        results = PRODUCTS
    return render_template('home.html', products=results, cart_count=get_cart_count(), search_query=q, current_category=None, display_category=None)
    
if __name__ == '__main__':
    app.run(debug=True)