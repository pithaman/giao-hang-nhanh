# ============================================
# IMPORTS - PHẢI Ở ĐẦU FILE
# ============================================
from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================
# CLASS USER
# ============================================
class User(db.Model, UserMixin):
    __tablename__ = 'nguoi_dung'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mat_khau = db.Column(db.String(255), nullable=False)
    vai_tro = db.Column(db.Enum('admin', 'khach_hang', 'tai_xe'), nullable=False)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_cap_nhat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    khach_hang = db.relationship('KhachHang', backref='user', uselist=False, cascade='all, delete-orphan')
    tai_xe = db.relationship('TaiXe', backref='user', uselist=False, cascade='all, delete-orphan')
    thong_baos = db.relationship('ThongBao', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    # Flask-Login methods
    def get_id(self):
        return str(self.id)
    
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.mat_khau = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.mat_khau, password)
    
    def is_admin(self):
        return self.vai_tro == 'admin'
    
    def is_customer(self):
        return self.vai_tro == 'khach_hang'
    
    def is_driver(self):
        return self.vai_tro == 'tai_xe'


# ============================================
# CLASS KHACHHANG
# ============================================
class KhachHang(db.Model):
    __tablename__ = 'khach_hang'
    
    id = db.Column(db.Integer, primary_key=True)
    nguoi_dung_id = db.Column(db.Integer, db.ForeignKey('nguoi_dung.id'), nullable=False)
    ho_ten = db.Column(db.String(100), nullable=False)
    so_dien_thoai = db.Column(db.String(20), nullable=False)
    dia_chi = db.Column(db.Text)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_cap_nhat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    don_hangs = db.relationship('DonHang', backref='khach_hang', lazy=True, foreign_keys='DonHang.khach_hang_id')
    
    def __repr__(self):
        return f'<KhachHang {self.ho_ten}>'


# ============================================
# CLASS TAIXE
# ============================================
class TaiXe(db.Model):
    __tablename__ = 'tai_xe'
    
    id = db.Column(db.Integer, primary_key=True)
    nguoi_dung_id = db.Column(db.Integer, db.ForeignKey('nguoi_dung.id'), nullable=False)
    ho_ten = db.Column(db.String(100), nullable=False)
    so_dien_thoai = db.Column(db.String(20), nullable=False)
    bien_so_xe = db.Column(db.String(20), unique=True)
    loai_xe = db.Column(db.Enum('xe_may', 'o_to', 'xe_tai'), default='xe_may')
    trang_thai = db.Column(db.Enum('hoat_dong', 'ngung_hoat_dong', 'tam_dung'), default='hoat_dong')
    danh_gia = db.Column(db.Numeric(3,2), default=0.00)
    tong_don = db.Column(db.Integer, default=0)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_cap_nhat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    don_hangs = db.relationship('DonHang', backref='tai_xe', lazy=True)
    vi_tris = db.relationship('ViTriTaiXe', backref='tai_xe', lazy=True)
    danh_gias = db.relationship('DanhGia', backref='tai_xe', lazy=True)
    
    def __repr__(self):
        return f'<TaiXe {self.ho_ten}>'


# ============================================
# CLASS KHUYENMAI
# ============================================
class KhuyenMai(db.Model):
    __tablename__ = 'khuyen_mai'
    
    id = db.Column(db.Integer, primary_key=True)
    ma_khuyen_mai = db.Column(db.String(20), unique=True, nullable=False)
    loai_giam_gia = db.Column(db.Enum('phan_tram', 'co_dinh'), nullable=False)
    gia_tri_giam = db.Column(db.Numeric(10,0), nullable=False)
    don_toi_thieu = db.Column(db.Numeric(12,0), default=0)
    giam_toi_da = db.Column(db.Numeric(12,0), default=0)
    so_luong = db.Column(db.Integer, default=100)
    so_luong_da_dung = db.Column(db.Integer, default=0)
    ngay_het_han = db.Column(db.DateTime, nullable=False)
    dang_hoat_dong = db.Column(db.Boolean, default=True)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    
    don_hangs = db.relationship('DonHang', backref='khuyen_mai', lazy=True)
    
    def __repr__(self):
        return f'<KhuyenMai {self.ma_khuyen_mai}>'
    
    def is_valid(self):
        from datetime import datetime
        return (self.dang_hoat_dong and 
                self.ngay_het_han > datetime.utcnow() and 
                self.so_luong_da_dung < self.so_luong)


# ============================================
# CLASS DONHANG
# ============================================
class DonHang(db.Model):
    __tablename__ = 'don_hang'
    
    id = db.Column(db.Integer, primary_key=True)
    khach_hang_id = db.Column(db.Integer, db.ForeignKey('khach_hang.id'), nullable=False)
    tai_xe_id = db.Column(db.Integer, db.ForeignKey('tai_xe.id'))
    khuyen_mai_id = db.Column(db.Integer, db.ForeignKey('khuyen_mai.id'))
    ma_don = db.Column(db.String(20), unique=True, nullable=False)
    dia_chi_lay = db.Column(db.Text, nullable=False)
    vi_do_lay = db.Column(db.Numeric(10,8))
    kinh_do_lay = db.Column(db.Numeric(11,8))
    dia_chi_giao = db.Column(db.Text, nullable=False)
    vi_do_giao = db.Column(db.Numeric(10,8))
    kinh_do_giao = db.Column(db.Numeric(11,8))
    khoang_cach = db.Column(db.Numeric(10,2))
    trang_thai = db.Column(db.Enum('cho_duyet', 'da_gan', 'dang_lay', 'dang_giao', 'hoan_thanh', 'da_huy'), default='cho_duyet')
    phi_van_chuyen = db.Column(db.Numeric(12,0), default=0)
    tien_hang = db.Column(db.Numeric(12,0), default=0)
    tien_giam_gia = db.Column(db.Numeric(12,0), default=0)
    tong_tien = db.Column(db.Numeric(12,0), nullable=False)
    ghi_chu = db.Column(db.Text)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_gan = db.Column(db.DateTime)
    ngay_hoan_thanh = db.Column(db.DateTime)
    ngay_huy = db.Column(db.DateTime)
    
    chi_tiet = db.relationship('ChiTietDon', backref='don_hang', lazy=True, cascade='all, delete-orphan')
    thanh_toan = db.relationship('ThanhToan', backref='don_hang', uselist=False, cascade='all, delete-orphan')
    danh_gia = db.relationship('DanhGia', backref='don_hang', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<DonHang {self.ma_don}>'
    
    def get_trang_thai_display(self):
        status_map = {
            'cho_duyet': 'Chờ duyệt',
            'da_gan': 'Đã gán',
            'dang_lay': 'Đang lấy',
            'dang_giao': 'Đang giao',
            'hoan_thanh': 'Hoàn thành',
            'da_huy': 'Đã hủy'
        }
        return status_map.get(self.trang_thai, self.trang_thai)


# ============================================
# CLASS CHITIETDON
# ============================================
class ChiTietDon(db.Model):
    __tablename__ = 'chi_tiet_don'
    
    id = db.Column(db.Integer, primary_key=True)
    don_hang_id = db.Column(db.Integer, db.ForeignKey('don_hang.id'), nullable=False)
    mo_ta = db.Column(db.String(255), nullable=False)
    trong_luong = db.Column(db.Numeric(6,2), default=0.00)
    so_luong = db.Column(db.Integer, default=1)
    gia = db.Column(db.Numeric(12,0), default=0)
    
    def __repr__(self):
        return f'<ChiTietDon {self.id}>'


# ============================================
# CLASS THANHTOAN
# ============================================
class ThanhToan(db.Model):
    __tablename__ = 'thanh_toan'
    
    id = db.Column(db.Integer, primary_key=True)
    don_hang_id = db.Column(db.Integer, db.ForeignKey('don_hang.id'), nullable=False)
    phuong_thuc = db.Column(db.Enum('tien_mat', 'chuyen_khoan', 'cod', 'momo', 'vnpay'), nullable=False)
    trang_thai = db.Column(db.Enum('cho_thanh_toan', 'da_thanh_toan', 'da_hoan_tien'), default='cho_thanh_toan')
    so_tien = db.Column(db.Numeric(12,0), nullable=False)
    ma_giao_dich = db.Column(db.String(100))
    ghi_chu = db.Column(db.Text)
    ngay_thanh_toan = db.Column(db.DateTime)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ThanhToan {self.id}>'


# ============================================
# CLASS VITRITAIXE
# ============================================
class ViTriTaiXe(db.Model):
    __tablename__ = 'vi_tri_tai_xe'
    
    id = db.Column(db.Integer, primary_key=True)
    tai_xe_id = db.Column(db.Integer, db.ForeignKey('tai_xe.id'), nullable=False)
    vi_do = db.Column(db.Numeric(10,8), nullable=False)
    kinh_do = db.Column(db.Numeric(11,8), nullable=False)
    do_chinh_xac = db.Column(db.Numeric(5,2))
    ngay_cap_nhat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ViTriTaiXe {self.tai_xe_id}>'


# ============================================
# CLASS THONGBAO
# ============================================
class ThongBao(db.Model):
    __tablename__ = 'thong_bao'
    
    id = db.Column(db.Integer, primary_key=True)
    nguoi_dung_id = db.Column(db.Integer, db.ForeignKey('nguoi_dung.id'), nullable=False)
    tieu_de = db.Column(db.String(100), nullable=False)
    noi_dung = db.Column(db.Text)
    loai = db.Column(db.Enum('don_hang', 'he_thong', 'khuyen_mai'), default='he_thong')
    da_doc = db.Column(db.Boolean, default=False)
    duong_dan = db.Column(db.String(255))
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ThongBao {self.tieu_de}>'


# ============================================
# CLASS DANHGIA
# ============================================
class DanhGia(db.Model):
    __tablename__ = 'danh_gia'
    
    id = db.Column(db.Integer, primary_key=True)
    don_hang_id = db.Column(db.Integer, db.ForeignKey('don_hang.id'), nullable=False, unique=True)
    khach_hang_id = db.Column(db.Integer, db.ForeignKey('khach_hang.id'), nullable=False)
    tai_xe_id = db.Column(db.Integer, db.ForeignKey('tai_xe.id'), nullable=False)
    diem_so = db.Column(db.Numeric(2,1), nullable=False)
    nhan_xet = db.Column(db.Text)
    ngay_danh_gia = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DanhGia {self.diem_so} sao>'