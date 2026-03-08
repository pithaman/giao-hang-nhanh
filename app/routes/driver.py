from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import DonHang, TaiXe, User, KhachHang
from datetime import datetime
from sqlalchemy import case



bp = Blueprint('driver', __name__)

@bp.route('/')
def home():
    """Trang chủ Driver - Dashboard"""
    if 'driver_id' not in session:
        return redirect(url_for('driver.login'))
    
    tai_xe = TaiXe.query.get(session['driver_id'])
    
    # Thống kê
    don_dang_giao = DonHang.query.filter_by(
        tai_xe_id=tai_xe.id, 
        trang_thai='dang_giao'
    ).count()
    
    don_hoan_thanh = DonHang.query.filter_by(
        tai_xe_id=tai_xe.id, 
        trang_thai='hoan_thanh'
    ).count()
    
    # Đơn đang giao
    don_hangs_dang_giao = DonHang.query.filter_by(
        tai_xe_id=tai_xe.id
    ).filter(
        DonHang.trang_thai.in_(['dang_lay', 'dang_giao'])
    ).order_by(DonHang.ngay_tao.desc()).all()
    
    return render_template('driver/home.html', 
                           tai_xe=tai_xe,
                           don_dang_giao=don_dang_giao,
                           don_hoan_thanh=don_hoan_thanh,
                           don_hangs_dang_giao=don_hangs_dang_giao)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Driver login"""
    if request.method == 'POST':
        so_dien_thoai = request.form.get('so_dien_thoai')
        mat_khau = request.form.get('mat_khau')
        
        # Tìm user với số điện thoại
        user = User.query.filter_by(email=f'driver_{so_dien_thoai}@temp.com').first()
        
        if user and user.vai_tro == 'tai_xe':
            tai_xe = TaiXe.query.filter_by(nguoi_dung_id=user.id).first()
            if tai_xe:
                session['driver_id'] = tai_xe.id
                session['driver_name'] = tai_xe.ho_ten
                flash(f'✅ Đăng nhập thành công! Chào {tai_xe.ho_ten}', 'success')
                return redirect(url_for('driver.home'))
        
        flash('❌ Số điện thoại hoặc mật khẩu không đúng', 'danger')
    
    return render_template('driver/login.html')

@bp.route('/logout')
def logout():
    """Driver logout"""
    session.pop('driver_id', None)
    session.pop('driver_name', None)
    flash('✅ Đã đăng xuất', 'info')
    return redirect(url_for('driver.login'))

@bp.route('/available-orders')
def available_orders():
    """Danh sách đơn hàng có thể nhận"""
    if 'driver_id' not in session:
        return redirect(url_for('driver.login'))
    
    # Đơn chưa có tài xế hoặc đang chờ gán
    don_hangs = DonHang.query.filter_by(
        tai_xe_id=None,
        trang_thai='cho_duyet'
    ).order_by(DonHang.ngay_tao.desc()).all()
    
    return render_template('driver/available_orders.html', don_hangs=don_hangs)

@bp.route('/accept-order/<int:order_id>', methods=['POST'])
def accept_order(order_id):
    """Tài xế nhận đơn"""
    if 'driver_id' not in session:
        return redirect(url_for('driver.login'))
    
    don_hang = DonHang.query.get_or_404(order_id)
    tai_xe = TaiXe.query.get(session['driver_id'])
    
    if don_hang.trang_thai == 'cho_duyet':
        don_hang.tai_xe_id = tai_xe.id
        don_hang.trang_thai = 'da_gan'
        don_hang.ngay_gan = datetime.utcnow()
        
        try:
            db.session.commit()
            flash(f'✅ Đã nhận đơn {don_hang.ma_don}', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Lỗi: {str(e)}', 'danger')
    else:
        flash('❌ Đơn hàng này đã được gán', 'warning')
    
    return redirect(url_for('driver.available_orders'))

@bp.route('/my-deliveries')
def my_deliveries():
    """Danh sách đơn đang giao"""
    if 'driver_id' not in session:
        return redirect(url_for('driver.login'))
    
    tai_xe = TaiXe.query.get(session['driver_id'])
    
    # Tất cả đơn của tài xế này
    don_hangs = DonHang.query.filter_by(
        tai_xe_id=tai_xe.id
    ).filter(
        DonHang.trang_thai.in_(['da_gan', 'dang_lay', 'dang_giao'])
    ).order_by(
        case(
            (DonHang.trang_thai == 'dang_giao', 1),
            (DonHang.trang_thai == 'dang_lay', 2),
            (DonHang.trang_thai == 'da_gan', 3),
            else_=4
        )
    ).all()
    
    return render_template('driver/my_deliveries.html', 
                           tai_xe=tai_xe, 
                           don_hangs=don_hangs)

@bp.route('/update-status/<int:order_id>', methods=['GET', 'POST'])
def update_status(order_id):
    """Cập nhật trạng thái đơn hàng"""
    if 'driver_id' not in session:
        return redirect(url_for('driver.login'))
    
    don_hang = DonHang.query.get_or_404(order_id)
    tai_xe = TaiXe.query.get(session['driver_id'])
    
    if request.method == 'POST':
        new_status = request.form.get('trang_thai')
        
        # Validate transition
        valid_transitions = {
            'da_gan': ['dang_lay'],
            'dang_lay': ['dang_giao'],
            'dang_giao': ['hoan_thanh', 'da_huy']
        }
        
        if new_status in valid_transitions.get(don_hang.trang_thai, []):
            don_hang.trang_thai = new_status
            
            if new_status == 'hoan_thanh':
                don_hang.ngay_hoan_thanh = datetime.utcnow()
                tai_xe.tong_don += 1
            elif new_status == 'da_huy':
                don_hang.ngay_huy = datetime.utcnow()
            
            try:
                db.session.commit()
                flash(f'✅ Cập nhật trạng thái thành công', 'success')
                return redirect(url_for('driver.my_deliveries'))
            except Exception as e:
                db.session.rollback()
                flash(f'❌ Lỗi: {str(e)}', 'danger')
        else:
            flash('❌ Chuyển trạng thái không hợp lệ', 'warning')
    
    return render_template('driver/update_status.html', don_hang=don_hang)

@bp.route('/completed')
def completed_orders():
    """Lịch sử đơn đã hoàn thành"""
    if 'driver_id' not in session:
        return redirect(url_for('driver.login'))
    
    tai_xe = TaiXe.query.get(session['driver_id'])
    
    don_hangs = DonHang.query.filter_by(
        tai_xe_id=tai_xe.id,
        trang_thai='hoan_thanh'
    ).order_by(DonHang.ngay_hoan_thanh.desc()).limit(20).all()
    
    return render_template('driver/completed_orders.html', 
                           tai_xe=tai_xe, 
                           don_hangs=don_hangs)

