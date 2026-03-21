# config.py
import os
from dotenv import load_dotenv

# Load environment variables từ .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'giao-hang-nhanh-secret-2026')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-2026')
    
    # ✅ MySQL Configuration - Build connection string từ các biến riêng
    mysql_user = os.environ.get('MYSQL_USER', 'giao_hang_user')
    mysql_password = os.environ.get('MYSQL_PASSWORD', '')
    mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
    mysql_port = os.environ.get('MYSQL_PORT', '3306')
    mysql_db = os.environ.get('MYSQL_DB', 'giao_hang_nhanh')
    
    # Ưu tiên dùng DATABASE_URL nếu có (cho production)
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url and database_url.startswith('mysql'):
        # Dùng full connection string từ env var
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Build connection string từ các biến riêng (cho local dev)
        # Format: mysql+pymysql://user:pass@host:port/db
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}'
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Kiểm tra connection trước khi dùng
        'pool_recycle': 300,    # Recycle connection sau 5 phút
    }
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False