from flask import Blueprint, request, jsonify
from db import get_db

user_bp = Blueprint("users", __name__)

# GET all users
@user_bp.route("/", methods=["GET"])
def get_users():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT user_id, full_name, email, role, created_at FROM users")
    users = cursor.fetchall()
    return jsonify(users)

# GET user by id
@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT user_id, full_name, email, role, created_at FROM users WHERE user_id=%s", (user_id,))
    user = cursor.fetchone()
    return jsonify(user) if user else ({"error": "Not found"}, 404)

# CREATE user
@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (full_name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
        (data["full_name"], data["email"], data["password_hash"], data.get("role", "customer"))
    )
    db.commit()
    return {"message": "User created", "user_id": cursor.lastrowid}, 201

# UPDATE user
@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE users SET full_name=%s, email=%s, role=%s WHERE user_id=%s",
        (data["full_name"], data["email"], data.get("role", "customer"), user_id)
    )
    db.commit()
    return {"message": "User updated"}

# DELETE user
@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
    db.commit()
    return {"message": "User deleted"}
