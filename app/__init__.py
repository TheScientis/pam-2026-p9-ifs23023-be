from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # CORS - izinkan semua origin (cocok untuk dev Flutter)
    CORS(app,
         resources={r"/*": {"origins": "*"}},
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         supports_credentials=False)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    # Inisialisasi database
    db.init_app(app)

    # Daftarkan semua blueprint/route
    from app.routes.motivation_routes import motivation_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(motivation_bp)
    app.register_blueprint(auth_bp)

    # Buat tabel & seed admin awal
    with app.app_context():
        db.create_all()
        _seed_admin()

    return app


def _seed_admin():
    """Buat akun admin default jika belum ada."""
    from app.models.user import User
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin")
        admin.set_password("motivation123")
        db.session.add(admin)
        db.session.commit()
        print("✅ Akun admin dibuat: username=admin, password=motivation123")
