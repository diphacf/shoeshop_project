from flask import Blueprint, request, jsonify
from db import get_db

product_bp = Blueprint("products", __name__)

# GET all products
@product_bp.route("/", methods=["GET"])
def get_products_api():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return jsonify(products)

# GET product by id
@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product_api(product_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

# CREATE product
@product_bp.route("/", methods=["POST"])
def create_product():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, category, image, description) VALUES (%s, %s, %s, %s, %s)",
        (data["name"], data["price"], data["category"], data.get("image", ""), data.get("description", ""))
    )
    db.commit()
    cursor.close()
    return jsonify({"message": "Product created"}), 201

# UPDATE product
@product_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE products SET name=%s, price=%s, category=%s, image=%s, description=%s WHERE product_id=%s",
        (data["name"], data["price"], data["category"], data.get("image", ""), data.get("description", ""), product_id)
    )
    db.commit()
    cursor.close()
    return jsonify({"message": "Product updated"})

# DELETE product
@product_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
    db.commit()
    cursor.close()