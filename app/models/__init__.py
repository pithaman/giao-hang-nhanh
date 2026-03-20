# app/models/__init__.py
from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    vai_tro = db.Column(db.String(20), nullable=False, default='customer')  # String!
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    don_hangs = db.relationship('DonHang', backref='customer', lazy='dynamic', foreign_keys='DonHang.customer_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class TaiXe(db.Model):
    __tablename__ = 'tai_xe'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    bien_so = db.Column(db.String(20))
    loai_xe = db.Column(db.String(50), default='xe_may')
    status = db.Column(db.String(20), default='pending')
    tong_don = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    
    user = db.relationship('User', backref='tai_xe_profile')


class DonHang(db.Model):
    __tablename__ = 'don_hang'
    
    id = db.Column(db.Integer, primary_key=True)
    ma_don = db.Column(db.String(20), unique=True, nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tai_xe_id = db.Column(db.Integer, db.ForeignKey('tai_xe.id'), nullable=True)
    
    dia_chi_lay = db.Column(db.String(255), nullable=False)
    dia_chi_giao = db.Column(db.String(255), nullable=False)
    loai_hang = db.Column(db.String(100))
    can_nang = db.Column(db.Float)
    ghi_chu = db.Column(db.Text)
    
    service_type = db.Column(db.String(20), default='hoa_toc')
    gia_tien = db.Column(db.Float, nullable=False)
    phi_dich_vu = db.Column(db.Float, default=0)
    giam_gia = db.Column(db.Float, default=0)
    tong_tien = db.Column(db.Float, nullable=False)
    
    trang_thai = db.Column(db.String(30), default='cho_duyet')  # String!
    
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_duyet = db.Column(db.DateTime)
    ngay_gan = db.Column(db.DateTime)
    ngay_hoan_thanh = db.Column(db.DateTime)
    ngay_huy = db.Column(db.DateTime)
    
    tai_xe = db.relationship('TaiXe', backref='don_hangs')
    
    def generate_ma_don(self):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f'DH{timestamp}{self.id:04d}'