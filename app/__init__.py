# app/__init__.py
from flask import Flask
from config import Config
from app.extensions import db, migrate, login_manager, jwt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    
    # Import routes
    from app.routes import auth, admin, customer, driver
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(customer.bp, url_prefix='/customer')
    app.register_blueprint(driver.bp, url_prefix='/driver')
    
    # User loader
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app