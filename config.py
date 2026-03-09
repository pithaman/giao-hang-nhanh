import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'giao-hang-nhanh-secret-2026')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-2026')
    
    # ✅ QUAN TRỌNG NHẤT - PHẢI CÓ DÒNG NÀY:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///giao_hang.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False