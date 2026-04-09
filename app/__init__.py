# app/__init__.py
from flask import Flask, redirect, url_for
from config import Config
from app.extensions import db, migrate, login_manager, jwt
import os
from dotenv import load_dotenv
from flask_login import LoginManager, current_user

load_dotenv()

login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    
    # ✅ USER LOADER - BẮT BUỘC CHO FLASK-LOGIN
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.routes.customer import bp as customer_bp
    app.register_blueprint(customer_bp, url_prefix='/customer')
    
    from app.routes.driver import bp as driver_bp
    app.register_blueprint(driver_bp, url_prefix='/driver')
    
    # ✅ ERROR HANDLER CHO 403 FORBIDDEN
    @app.errorhandler(403)
    def forbidden_error(error):
        """Xử lý khi user không có quyền truy cập"""
        if current_user.is_authenticated:
            if current_user.vai_tro == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif current_user.vai_tro == 'customer':
                return redirect(url_for('customer.dashboard'))
            elif current_user.vai_tro == 'driver':
                return redirect(url_for('driver.dashboard'))
        return redirect(url_for('auth.login'))
    
    # ✅ CẤU HÌNH DATABASE ĐƠN GIẢN (TƯƠNG THÍCH POSTGRESQL + MYSQL)
    database_url = os.environ.get('DATABASE_URL')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,      # Tự động reconnect nếu mất kết nối
        "pool_recycle": 300,         # Recycle connection sau 300 giây
        # ✅ KHÔNG CẦN connect_args SSL cho PostgreSQL trên Render!
    }
    
    # Tạo database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created!")
        except Exception as e:
            print(f"⚠️ Warning creating tables: {e}")
        
        from app.models import User
        if not User.query.filter_by(vai_tro='admin').first():
            admin = User(
                name='Admin',
                email='admin@giaohang.com',
                phone='0900000000',
                vai_tro='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("ℹ️ Admin default created")
    
    return app  # ← Phải ở CUỐI CÙNG