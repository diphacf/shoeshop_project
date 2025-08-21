import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="369024",
        database="shoeshop_db"
    )
    return conn