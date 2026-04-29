from flask import Blueprint, request, jsonify
from app.services.motivation_service import (
    create_motivations,
    get_all_motivations,
    get_motivation_by_id,
    delete_motivation
)
from app.middleware.auth_middleware import token_required

motivation_bp = Blueprint("motivation", __name__)


@motivation_bp.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "AI Motivation API berjalan!",
        "version": "1.0.0",
        "endpoints": {
            "POST /auth/register": "Registrasi akun baru",
            "POST /auth/login": "Login dan dapatkan token",
            "GET  /auth/verify": "Verifikasi token (auth required)",
            "POST /motivations/generate": "Generate motivasi baru (auth required)",
            "GET  /motivations": "Ambil semua motivasi (auth required)",
            "GET  /motivations/<id>": "Ambil motivasi by ID (auth required)",
            "DELETE /motivations/<id>": "Hapus motivasi (auth required)"
        }
    })


@motivation_bp.route("/motivations/generate", methods=["POST"])
@token_required
def generate():
    """Generate kata-kata motivasi baru menggunakan Gemini AI."""
    data = request.get_json()
    theme = data.get("theme", "").strip()
    total = data.get("total")

    if not theme:
        return jsonify({"error": "Theme wajib diisi"}), 400

    if total is None:
        return jsonify({"error": "Total wajib diisi"}), 400

    if not isinstance(total, int) or total <= 0:
        return jsonify({"error": "Total harus berupa angka lebih dari 0"}), 400

    if total > 10:
        return jsonify({"error": "Total maksimal adalah 10"}), 400

    try:
        result = create_motivations(theme, total, user_id=request.user_id)
        return jsonify({
            "message": f"Berhasil generate {len(result)} motivasi",
            "theme": theme,
            "total": len(result),
            "data": result
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@motivation_bp.route("/motivations", methods=["GET"])
@token_required
def get_all():
    """Ambil semua motivasi dengan pagination dan optional filter kategori."""
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    category = request.args.get("category", default=None, type=str)

    if per_page > 50:
        return jsonify({"error": "per_page maksimal adalah 50"}), 400

    try:
        data = get_all_motivations(page=page, per_page=per_page, category=category)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@motivation_bp.route("/motivations/<int:motivation_id>", methods=["GET"])
@token_required
def get_one(motivation_id):
    """Ambil satu motivasi berdasarkan ID."""
    try:
        data = get_motivation_by_id(motivation_id)
        if not data:
            return jsonify({"error": "Motivasi tidak ditemukan"}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@motivation_bp.route("/motivations/<int:motivation_id>", methods=["DELETE"])
@token_required
def remove(motivation_id):
    """Hapus motivasi berdasarkan ID."""
    try:
        success = delete_motivation(motivation_id)
        if not success:
            return jsonify({"error": "Motivasi tidak ditemukan"}), 404
        return jsonify({"message": "Motivasi berhasil dihapus"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
