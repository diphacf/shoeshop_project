import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "369024"),
    "database": os.getenv("DB_NAME", "shoestore"),
    "port": int(os.getenv("DB_PORT", "3306")),
}