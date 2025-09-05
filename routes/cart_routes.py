from flask import Blueprint, request, jsonify
from db import get_db

cart_bp = Blueprint("cart", __name__)

# GET cart by user
@cart_bp.route("/<int:user_id>", methods=["GET"])
def get_cart(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.cart_id, c.product_id, p.product_name, c.quantity, p.price, (c.quantity * p.price) AS total
        FROM cart c
        JOIN products p ON c.product_id = p.product_id
        WHERE c.user_id=%s
    """, (user_id,))
    items = cursor.fetchall()
    return jsonify(items)

# ADD to cart
@cart_bp.route("/", methods=["POST"])
def add_to_cart():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
        (data["user_id"], data["product_id"], data["quantity"])
    )
    db.commit()
    return {"message": "Item added to cart", "cart_id": cursor.lastrowid}, 201

# UPDATE quantity
@cart_bp.route("/<int:cart_id>", methods=["PUT"])
def update_cart(cart_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE cart SET quantity=%s WHERE cart_id=%s",
        (data["quantity"], cart_id)
    )
    db.commit()
    return {"message": "Cart updated"}

# DELETE item
@cart_bp.route("/<int:cart_id>", methods=["DELETE"])
def delete_cart(cart_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM cart WHERE cart_id=%s", (cart_id,))
    db.commit()
    return {"message": "Cart item deleted"}
