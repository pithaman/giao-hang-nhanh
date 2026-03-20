# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'giao-hang-nhanh-secret-2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///giao_hang.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-2026')