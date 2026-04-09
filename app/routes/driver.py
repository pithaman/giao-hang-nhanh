# app/routes/driver.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, logout_user  # ✅ THÊM logout_user
from app.models import TaiXe, DonHang
from app.extensions import db
from datetime import datetime

bp = Blueprint('driver', __name__, url_prefix='/driver')

@bp.route('/')
@login_required
def dashboard():
    """Trang chủ của tài xế"""
    
    # ✅ CHECK ROLE - LOGOUT TRƯỚC KHI REDIRECT ĐỂ TRÁNH LOOP
    if current_user.vai_tro != 'driver':
        logout_user()  # ← QUAN TRỌNG: Logout để phá vòng lặp!
        flash('❌ Bạn không có quyền truy cập trang tài xế!', 'error')
        return redirect(url_for('auth.login'))
    
    # Lấy object TaiXe của user hiện tại
    tai_xe = TaiXe.query.filter_by(user_id=current_user.id).first()
    
    # ✅ CHECK PROFILE TÀI XẾ
    if not tai_xe:
        logout_user()  # ← Logout nếu không có profile
        flash('❌ Tài khoản chưa được đăng ký làm tài xế!', 'error')
        return redirect(url_for('auth.login'))
    
    # Nếu tài khoản chưa được Admin duyệt
    if tai_xe.status != 'approved':
        flash('⏳ Tài khoản đang chờ Admin duyệt!', 'warning')
        return render_template('driver/pending.html')
    
    # === THỐNG KÊ ===
    don_hang_cua_toi = DonHang.query.filter_by(tai_xe_id=tai_xe.id).all()
    so_don_hoan_thanh = len([d for d in don_hang_cua_toi if d.trang_thai == 'hoan_thanh'])
    so_don_dang_giao = len([d for d in don_hang_cua_toi if d.trang_thai in ['da_gan', 'dang_lay_hang', 'dang_giao']])
    doanh_thu = so_don_hoan_thanh * 20000 

    return render_template('driver/dashboard.html', 
                           tai_xe=tai_xe,
                           so_don_hoan_thanh=so_don_hoan_thanh,
                           so_don_dang_giao=so_don_dang_giao,
                           doanh_thu=doanh_thu)


@bp.route('/orders')
@login_required
def orders():
    """Danh sách đơn hàng"""
    
    if current_user.vai_tro != 'driver':
        logout_user()
        flash('❌ Bạn không có quyền truy cập!', 'error')
        return redirect(url_for('auth.login'))
    
    tai_xe = TaiXe.query.filter_by(user_id=current_user.id).first()
    if not tai_xe:
        logout_user()
        flash('❌ Chưa có thông tin tài xế!', 'error')
        return redirect(url_for('auth.login'))

    status_filter = request.args.get('status', 'all')
    query = DonHang.query.filter_by(tai_xe_id=tai_xe.id)
    if status_filter != 'all':
        query = query.filter_by(trang_thai=status_filter)
    don_hangs = query.order_by(DonHang.ngay_tao.desc()).all()
    
    return render_template('driver/orders.html', don_hangs=don_hangs, current_status=status_filter)


@bp.route('/order/<int:id>/update', methods=['POST'])
@login_required
def update_order_status(id):
    """Cập nhật trạng thái đơn"""
    
    if current_user.vai_tro != 'driver':
        logout_user()
        return redirect(url_for('auth.login'))
    
    tai_xe = TaiXe.query.filter_by(user_id=current_user.id).first()
    if not tai_xe:
        logout_user()
        return redirect(url_for('auth.login'))

    don_hang = DonHang.query.get_or_404(id)
    if don_hang.tai_xe_id != tai_xe.id:
        flash('❌ Bạn không có quyền sửa đơn này!', 'error')
        return redirect(url_for('driver.orders'))

    new_status = request.form.get('new_status')
    if new_status == 'da_lay_hang':
        don_hang.trang_thai = 'dang_lay_hang'
        flash('✅ Đã lấy hàng!', 'success')
    elif new_status == 'dang_giao':
        don_hang.trang_thai = 'dang_giao'
        flash('🚚 Đang giao!', 'info')
    elif new_status == 'hoan_thanh':
        don_hang.trang_thai = 'hoan_thanh'
        don_hang.ngay_hoan_thanh = datetime.utcnow()
        flash('🎉 Đã giao xong!', 'success')
    elif new_status == 'huy':
        don_hang.trang_thai = 'da_huy'
        don_hang.tai_xe_id = None
        flash('❌ Đã hủy', 'warning')

    db.session.commit()
    return redirect(url_for('driver.orders'))