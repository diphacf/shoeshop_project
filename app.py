from flask import Flask, flash, redirect, render_template, url_for, request, session
import unicodedata
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    return render_template('dangky.html')

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
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Xử lý đăng nhập đơn giản (cần kết nối database thật)
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
    
    # Xử lý đăng ký đơn giản (cần kết nối database thật)
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
def admin():
    return render_template('admin.html')

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
    quantity = request.form.get('quantity', 1)
    
    if not product_id:
        flash('Có lỗi xảy ra khi thêm sản phẩm vào giỏ hàng!', 'error')
        return redirect(url_for('home'))
    
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
    product_id = request.form.get('product_id')
    size = request.form.get('size')
    
    if 'cart' in session:
        cart = session['cart']
        # Tìm và xóa sản phẩm khỏi giỏ hàng
        cart = [item for item in cart if not (item['product_id'] == int(product_id) and item.get('size') == size)]
        session['cart'] = cart
        flash('Đã xóa sản phẩm khỏi giỏ hàng!', 'success')
    
    return redirect(url_for('giohang'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    """Cập nhật số lượng sản phẩm trong giỏ hàng"""
    product_id = request.form.get('product_id')
    size = request.form.get('size')
    quantity = request.form.get('quantity')
    
    if 'cart' in session and quantity and int(quantity) > 0:
        cart = session['cart']
        for item in cart:
            if item['product_id'] == int(product_id) and item.get('size') == size:
                item['quantity'] = int(quantity)
                break
        session['cart'] = cart
        flash('Đã cập nhật giỏ hàng!', 'success')
    elif int(quantity) <= 0:
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