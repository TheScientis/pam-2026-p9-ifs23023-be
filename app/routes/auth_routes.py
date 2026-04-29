from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
import jwt
import datetime
import os

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = os.getenv("SECRET_KEY", "motivation-app-secret-key")

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    """Endpoint registrasi user baru."""
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "Username dan password wajib diisi"}), 400

    if len(username) < 3:
        return jsonify({"error": "Username minimal 3 karakter"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password minimal 6 karakter"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username sudah digunakan"}), 409

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    token = generate_token(new_user.id)
    return jsonify({
        "message": "Registrasi berhasil",
        "token": token,
        "username": new_user.username
    }), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """Endpoint login user."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username dan password wajib diisi"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Username atau password salah"}), 401

    token = generate_token(user.id)
    return jsonify({
        "message": "Login berhasil",
        "token": token,
        "username": user.username
    })


@auth_bp.route("/auth/verify", methods=["GET"])
def verify():
    """Endpoint verifikasi token."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token tidak ditemukan"}), 401

    token = auth_header.split(" ")[1]
    user_id = verify_token(token)

    if not user_id:
        return jsonify({"error": "Token tidak valid atau sudah expired"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User tidak ditemukan"}), 404

    return jsonify({
        "message": "Token valid",
        "username": user.username,
        "user_id": user.id
    })
