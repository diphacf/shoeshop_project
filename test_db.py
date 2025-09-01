from db import get_db
from werkzeug.security import generate_password_hash

try:
    conn = get_db()
    cursor = conn.cursor()

    username = "Test User"
    email = "test@example.com"
    password = generate_password_hash("123456")

    cursor.execute(
        "INSERT INTO users (full_name, email, password_hash) VALUES (%s, %s, %s)",
        (username, email, password)
    )
    conn.commit()

    print("✅ Thêm user thành công!")
    cursor.close()
    conn.close()
except Exception as e:
    print("❌ Lỗi:", e)
