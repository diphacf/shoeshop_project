from flask import Blueprint, request, jsonify
from db import get_db

order_bp = Blueprint("orders", __name__)

# GET all orders
@order_bp.route("/", methods=["GET"])
def get_orders():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    return jsonify(orders)

# GET order by id
@order_bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders WHERE order_id=%s", (order_id,))
    order = cursor.fetchone()
    return jsonify(order) if order else ({"error": "Not found"}, 404)

# CREATE order
@order_bp.route("/", methods=["POST"])
def create_order():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO orders (user_id, total_amount, note, status) VALUES (%s, %s, %s, %s)",
        (data["user_id"], data["total_amount"], data.get("note"), data.get("status", "pending"))
    )
    db.commit()
    return {"message": "Order created", "order_id": cursor.lastrowid}, 201

# UPDATE order
@order_bp.route("/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE orders SET status=%s, note=%s, total_amount=%s WHERE order_id=%s",
        (data.get("status"), data.get("note"), data.get("total_amount"), order_id)
    )
    db.commit()
    return {"message": "Order updated"}

# DELETE order
@order_bp.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM orders WHERE order_id=%s", (order_id,))
    db.commit()
    return {"message": "Order deleted"}
