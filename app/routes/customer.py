from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import DonHang, KhachHang, User, KhuyenMai
from datetime import datetime

bp = Blueprint('customer', __name__)

@bp.route('/')
def home():
    """Trang chủ Customer"""
    return render_template('customer/home.html')

@bp.route('/place-order', methods=['GET', 'POST'])
def place_order():
    """Đặt hàng mới"""
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        ho_ten = request.form.get('ho_ten')
        so_dien_thoai = request.form.get('so_dien_thoai')
        dia_chi_lay = request.form.get('dia_chi_lay')
        dia_chi_giao = request.form.get('dia_chi_giao')
        trong_luong = request.form.get('trong_luong', 1)
        mo_ta = request.form.get('mo_ta', '')
        phi_van_chuyen = request.form.get('phi_van_chuyen', 30000)
        ma_khuyen_mai = request.form.get('ma_khuyen_mai', '')
        
        # Tạo hoặc lấy customer
        user_email = f'customer_{so_dien_thoai}@temp.com'
        user = User.query.filter_by(email=user_email).first()
        
        if not user:
            user = User(
                email=user_email,
                mat_khau='temp123',
                vai_tro='khach_hang'
            )
            db.session.add(user)
            db.session.flush()
            
            khach_hang = KhachHang(
                nguoi_dung_id=user.id,
                ho_ten=ho_ten,
                so_dien_thoai=so_dien_thoai,
                dia_chi=dia_chi_giao
            )
            db.session.add(khach_hang)
            db.session.flush()
            khach_hang_id = khach_hang.id
        else:
            khach_hang = KhachHang.query.filter_by(nguoi_dung_id=user.id).first()
            khach_hang_id = khach_hang.id if khach_hang else None
        
        # Tạo mã đơn
        ma_don = 'DH' + datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Tính giảm giá nếu có
        tien_giam_gia = 0
        if ma_khuyen_mai:
            km = KhuyenMai.query.filter_by(
                ma_khuyen_mai=ma_khuyen_mai,
                dang_hoat_dong=True
            ).first()
            if km and km.is_valid():
                if km.loai_giam_gia == 'phan_tram':
                    tien_giam_gia = int(phi_van_chuyen * km.gia_tri_giam / 100)
                else:
                    tien_giam_gia = int(km.gia_tri_giam)
                
                # Update số lượng đã dùng
                km.so_luong_da_dung += 1
        
        tong_tien = int(phi_van_chuyen) - tien_giam_gia
        
        # Tạo đơn hàng
        don_hang = DonHang(
            khach_hang_id=khach_hang_id,
            ma_don=ma_don,
            dia_chi_lay=dia_chi_lay,
            dia_chi_giao=dia_chi_giao,
            phi_van_chuyen=phi_van_chuyen,
            tien_hang=0,
            tien_giam_gia=tien_giam_gia,
            tong_tien=tong_tien,
            ghi_chu=mo_ta,
            trang_thai='cho_duyet'
        )
        
        try:
            db.session.add(don_hang)
            db.session.commit()
            flash('✅ Đặt hàng thành công! Mã đơn: ' + ma_don, 'success')
            return redirect(url_for('customer.order_success', ma_don=ma_don))
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Lỗi khi đặt hàng: {str(e)}', 'danger')
    
    return render_template('customer/place_order.html')

@bp.route('/order-success/<ma_don>')
def order_success(ma_don):
    """Xác nhận đặt hàng thành công"""
    don_hang = DonHang.query.filter_by(ma_don=ma_don).first_or_404()
    return render_template('customer/order_success.html', don_hang=don_hang)

@bp.route('/my-orders')
def my_orders():
    """Lịch sử đơn hàng"""
    # Lấy tất cả đơn hàng (sau này sẽ filter theo user đăng nhập)
    don_hangs = DonHang.query.order_by(DonHang.ngay_tao.desc()).limit(10).all()
    return render_template('customer/my_orders.html', don_hangs=don_hangs)

@bp.route('/track-order/<ma_don>')
def track_order(ma_don):
    """Theo dõi đơn hàng"""
    don_hang = DonHang.query.filter_by(ma_don=ma_don).first_or_404()
    return render_template('customer/track_order.html', don_hang=don_hang)

@bp.route('/calculate-fee')
def calculate_fee():
    """Tính phí vận chuyển (AJAX)"""
    khoang_cach = float(request.args.get('distance', 5))
    trong_luong = float(request.args.get('weight', 1))
    
    # Công thức tính phí đơn giản
    phi_co_ban = 30000  # 30k cho 5km đầu
    phi_km_them = 5000  # 5k mỗi km thêm
    phi_trong_luong = 5000  # 5k mỗi kg thêm
    
    phi_van_chuyen = phi_co_ban
    if khoang_cach > 5:
        phi_van_chuyen += (khoang_cach - 5) * phi_km_them
    if trong_luong > 1:
        phi_van_chuyen += (trong_luong - 1) * phi_trong_luong
    
    return {'phi_van_chuyen': int(phi_van_chuyen)}