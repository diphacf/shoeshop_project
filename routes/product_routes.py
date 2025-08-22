from flask import Blueprint, request, jsonify
from db import get_db

product_bp = Blueprint("products", __name__)

# GET all products
@product_bp.route("/", methods=["GET"])
def get_products():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return jsonify(products)

# GET product by id
@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()
    return jsonify(product) if product else ({"error": "Not found"}, 404)

# CREATE product
@product_bp.route("/", methods=["POST"])
def create_product():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO products (product_name, description, price, category_id, image_url) VALUES (%s, %s, %s, %s, %s)",
        (data["product_name"], data.get("description"), data["price"], data.get("category_id"), data.get("image_url"))
    )
    db.commit()
    return {"message": "Product created", "product_id": cursor.lastrowid}, 201

# UPDATE product
@product_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE products SET product_name=%s, description=%s, price=%s, category_id=%s, image_url=%s WHERE product_id=%s",
        (data["product_name"], data.get("description"), data["price"], data.get("category_id"), data.get("image_url"), product_id)
    )
    db.commit()
    return {"message": "Product updated"}

# DELETE product
@product_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
    db.commit()
    return {"message": "Product deleted"}
