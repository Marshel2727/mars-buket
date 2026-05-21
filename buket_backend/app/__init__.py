from flask import Flask
from app.config import Config, db_connection
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app =  Flask(__name__)

    # untuk menghubungkan ke database saat aplikasi dibuat
    app.config.from_object(Config)
    db_connection()

    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)
    CORS(app)
    # untruk memastikan koneksi ke database berhasil saat aplikasi dijalankan

    # Import model setelah inisialisasi db
    from app.models.user import User, Address_Book
    from app.models.product import Kategori, Product, VarianProduk, GaleriProduk

    # Import dan register blueprint setelah inisialisasi db
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.address_routes import address_bp
    app.register_blueprint(address_bp)

    from app.routes.product_routes import product_bp
    app.register_blueprint(product_bp)

    return app