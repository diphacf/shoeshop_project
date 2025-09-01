# Admin Configuration
# File này chứa cấu hình cho hệ thống admin

# Thông tin tài khoản admin mặc định
DEFAULT_ADMIN_CREDENTIALS = {
    'admin': 'admin123',  # username: password
    'admin@shoestore.com': 'admin123',  # email: password (for main login)
    # Bạn có thể thêm nhiều tài khoản admin khác
    # 'admin2': 'password456',
}

# Cấu hình bảo mật
ADMIN_SESSION_TIMEOUT = 7200  # 2 giờ (giây)
ADMIN_REMEMBER_ME_DAYS = 7    # 7 ngày

# Thông tin về ứng dụng
APP_NAME = "ShoeShop Admin"
APP_VERSION = "1.0.0"

# Cấu hình đăng nhập
LOGIN_ATTEMPTS_LIMIT = 5      # Số lần đăng nhập sai tối đa
LOGIN_LOCKOUT_TIME = 300      # Thời gian khóa (giây) sau khi đăng nhập sai quá nhiều

# Quyền admin (có thể mở rộng sau này)
ADMIN_PERMISSIONS = {
    'admin': [
        'view_products',
        'add_products', 
        'edit_products',
        'delete_products',
        'view_orders',
        'manage_orders',
        'view_users',
        'manage_users',
        'system_settings'
    ]
}

# Log admin actions (tùy chọn)
ENABLE_ADMIN_LOGGING = True
ADMIN_LOG_FILE = 'admin_actions.log'
