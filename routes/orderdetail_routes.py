from flask import Blueprint, request, jsonify
from db import get_db

orderdetail_bp = Blueprint("orderdetails", __name__)

# GET order details by order_id
@orderdetail_bp.route("/<int:order_id>", methods=["GET"])
def get_orderdetails(order_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT od.detail_id, od.product_id, p.product_name, od.quantity, od.price, (od.quantity * od.price) AS subtotal
        FROM orderdetails od
        JOIN products p ON od.product_id = p.product_id
        WHERE od.order_id=%s
    """, (order_id,))
    details = cursor.fetchall()
    return jsonify(details)

# ADD order detail
@orderdetail_bp.route("/", methods=["POST"])
def create_orderdetail():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO orderdetails (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
        (data["order_id"], data["product_id"], data["quantity"], data["price"])
    )
    db.commit()
    return {"message": "Order detail created", "detail_id": cursor.lastrowid}, 201

# UPDATE order detail
@orderdetail_bp.route("/<int:detail_id>", methods=["PUT"])
def update_orderdetail(detail_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE orderdetails SET quantity=%s, price=%s WHERE detail_id=%s",
        (data["quantity"], data["price"], detail_id)
    )
    db.commit()
    return {"message": "Order detail updated"}

# DELETE order detail
@orderdetail_bp.route("/<int:detail_id>", methods=["DELETE"])
def delete_orderdetail(detail_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM orderdetails WHERE detail_id=%s", (detail_id,))
    db.commit()
    return {"message": "Order detail deleted"}
