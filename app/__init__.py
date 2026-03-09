from flask import Flask
import os
from dotenv import load_dotenv

# Import extensions TỪ FILE RIÊNG
from app.extensions import db, migrate, login_manager, jwt

load_dotenv()

# Cấu hình login
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Vui lòng đăng nhập để tiếp tục.'

def create_app():
    app = Flask(__name__)
    
    # Config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'giao-hang-nhanh-secret-2026')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-2026')
    
    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    
    # Register blueprints
    from app.routes import auth, admin, customer, driver, api
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(customer.bp, url_prefix='/customer')
    app.register_blueprint(driver.bp, url_prefix='/driver')
    app.register_blueprint(api.bp, url_prefix='/api')
    
    return app