# config.py
import os
from dotenv import load_dotenv

# Load environment variables từ .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'giao-hang-nhanh-secret-2026')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-2026')
    
    # ✅ DEBUG: Log environment variables khi chạy
    _db_url = os.environ.get('DATABASE_URL')
    print(f"🔍 [CONFIG] DATABASE_URL from env: {_db_url[:50] + '...' if _db_url and len(_db_url) > 50 else _db_url}")
    
    if _db_url:
        # Dùng trực tiếp DATABASE_URL (hỗ trợ cả PostgreSQL và MySQL)
        SQLALCHEMY_DATABASE_URI = _db_url
        print(f"✅ [CONFIG] Using DATABASE_URL: {_db_url.split('://')[0]}://***@***")
    else:
        # Fallback: Build connection string từ các biến riêng (CHO LOCAL DEV)
        mysql_user = os.environ.get('MYSQL_USER', 'root')
        mysql_password = os.environ.get('MYSQL_PASSWORD', '')
        mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
        mysql_port = os.environ.get('MYSQL_PORT', '3306')
        mysql_db = os.environ.get('MYSQL_DB', 'giao_hang_nhanh')
        
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}'
        print(f"⚠️ [CONFIG] DATABASE_URL not set, falling back to: mysql+pymysql://***@{mysql_host}:{mysql_port}/{mysql_db}")
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False