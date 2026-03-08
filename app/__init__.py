from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager  # Thêm import
from flask_jwt_extended import JWTManager
from app.routes import api
app.register_blueprint(api.bp)

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()  # Tạo instance
login_manager.login_view = 'auth.login'  # Trang login mặc định

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)  # Init login manager
    
    # User loader for Flask-Login
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Import models
    with app.app_context():
        from app.models import User, KhachHang, TaiXe, DonHang, KhuyenMai
        from app.models import ChiTietDon, ThanhToan, ViTriTaiXe, ThongBao, DanhGia
    
    # Register blueprints
    from app.routes import auth, admin, customer, driver
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(customer.bp, url_prefix='/customer')
    app.register_blueprint(driver.bp, url_prefix='/driver')
    
    # Test route
    @app.route('/')
    def index():
        return render_template('home.html')
    
    return app

from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = 'giao-hang-nhanh-secret-key-2026'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
    
    jwt = JWTManager(app)  # Initialize JWT
    
    # ... rest of code