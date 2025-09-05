import pymysql
from pymysql import err
from config import Config

_pool = None

def get_db():
    global _pool
    if _pool is None:
        try:
            _pool = pymysql.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                autocommit=True,
                cursorclass=pymysql.cursors.DictCursor,
                charset='utf8mb4'
            )
        except err.OperationalError as e:
            # Auto-create database if missing (error code 1049)
            if getattr(e, 'args', [None])[0] == 1049:
                server = pymysql.connect(
                    host=Config.MYSQL_HOST,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    autocommit=True,
                    cursorclass=pymysql.cursors.DictCursor,
                    charset='utf8mb4'
                )
                with server.cursor() as cur:
                    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.MYSQL_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                server.close()
                _pool = pymysql.connect(
                    host=Config.MYSQL_HOST,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    database=Config.MYSQL_DB,
                    autocommit=True,
                    cursorclass=pymysql.cursors.DictCursor,
                    charset='utf8mb4'
                )
            else:
                raise
    return _pool

def ensure_schema():
    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fullname VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                phone VARCHAR(32) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """
        )