import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'giao-hang-nhanh-secret-2026')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-2026')
    
    # ✅ QUAN TRỌNG: Chỉ dùng SQLite, bỏ qua DATABASE_URL hoàn toàn
    SQLALCHEMY_DATABASE_URI = 'sqlite:///giao_hang.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cấu hình session
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'