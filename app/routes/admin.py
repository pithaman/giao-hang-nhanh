# app/routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import DonHang, TaiXe, User
from datetime import datetime, timedelta
from sqlalchemy import func

bp = Blueprint('admin', __name__)

@bp.route('/')
@login_required
def dashboard():
    """Dashboard thống kê tổng quan"""
    if current_user.vai_tro != 'admin':
        flash('❌ Bạn không có quyền truy cập!', 'error')
        return redirect(url_for('auth.login'))
    
    # === THỐNG KÊ TỔNG QUAN ===
    tong_don = DonHang.query.count()
    tong_khach = User.query.filter_by(vai_tro='customer').count()
    tong_tai_xe = TaiXe.query.count()
    
    # Doanh thu (chỉ tính đơn hoàn thành)
    tong_doanh_thu = db.session.query(db.func.sum(DonHang.tong_tien)).filter(
        DonHang.trang_thai == 'hoan_thanh'
    ).scalar() or 0
    
    # Đơn theo trạng thái
    don_cho_duyet = DonHang.query.filter_by(trang_thai='cho_duyet').count()
    don_dang_giao = DonHang.query.filter_by(trang_thai='dang_giao').count()
    don_hoan_thanh = DonHang.query.filter_by(trang_thai='hoan_thanh').count()
    don_da_huy = DonHang.query.filter_by(trang_thai='da_huy').count()
    
    # === ĐƠN THEO NGÀY (7 NGÀY GẦN NHẤT) ===
    ngay_gan_nhat = datetime.utcnow() - timedelta(days=7)
    don_theo_ngay = db.session.query(
        func.date(DonHang.ngay_tao).label('ngay'),
        func.count(DonHang.id).label('so_don'),
        func.sum(DonHang.tong_tien).label('doanh_thu')
    ).filter(
        DonHang.ngay_tao >= ngay_gan_nhat
    ).group_by(func.date(DonHang.ngay_tao)).all()
    
    # === TOP TÀI XẾ HIỆU SUẤT ===
    top_tai_xe = db.session.query(
        TaiXe.id,
        User.name,
        func.count(DonHang.id).label('tong_don'),
        TaiXe.rating,
        TaiXe.tong_don
    ).join(User, TaiXe.user_id == User.id
    ).outerjoin(DonHang, DonHang.tai_xe_id == TaiXe.id
    ).group_by(TaiXe.id, User.name, TaiXe.rating, TaiXe.tong_don
    ).order_by(func.count(DonHang.id).desc()
    ).limit(5).all()
    
    # === ĐƠN HÀNG MỚI NHẤT ===
    don_moi_nhat = DonHang.query.order_by(DonHang.ngay_tao.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
        tong_don=tong_don,
        tong_khach=tong_khach,
        tong_tai_xe=tong_tai_xe,
        tong_doanh_thu=tong_doanh_thu,
        don_cho_duyet=don_cho_duyet,
        don_dang_giao=don_dang_giao,
        don_hoan_thanh=don_hoan_thanh,
        don_da_huy=don_da_huy,
        don_theo_ngay=don_theo_ngay,
        top_tai_xe=top_tai_xe,
        don_moi_nhat=don_moi_nhat
    )

@bp.route('/orders')
@login_required
def orders():
    """Quản lý đơn hàng"""
    if current_user.vai_tro != 'admin':
        flash('❌ Bạn không có quyền!', 'error')
        return redirect(url_for('auth.login'))
    
    don_hangs = DonHang.query.order_by(DonHang.ngay_tao.desc()).all()
    return render_template('admin/orders.html', don_hangs=don_hangs)

@bp.route('/orders/<int:id>')
@login_required
def order_detail(id):
    """Chi tiết đơn hàng"""
    if current_user.vai_tro != 'admin':
        return redirect(url_for('auth.login'))
    
    don_hang = DonHang.query.get_or_404(id)
    return render_template('admin/order_detail.html', don_hang=don_hang)

@bp.route('/orders/<int:id>/approve', methods=['POST'])
@login_required
def approve_order(id):
    """Duyệt đơn hàng"""
    if current_user.vai_tro != 'admin':
        return redirect(url_for('auth.login'))
    
    don_hang = DonHang.query.get_or_404(id)
    don_hang.trang_thai = 'da_duyet'
    don_hang.ngay_duyet = datetime.utcnow()
    db.session.commit()
    
    flash('✅ Đã duyệt đơn hàng!', 'success')
    return redirect(url_for('admin.order_detail', id=id))

@bp.route('/orders/<int:id>/assign', methods=['GET', 'POST'])
@login_required
def assign_driver(id):
    """Gán tài xế cho đơn hàng"""
    if current_user.vai_tro != 'admin':
        return redirect(url_for('auth.login'))
    
    don_hang = DonHang.query.get_or_404(id)
    
    if request.method == 'POST':
        tai_xe_id = request.form.get('tai_xe_id')
        if tai_xe_id:
            don_hang.tai_xe_id = tai_xe_id
            don_hang.trang_thai = 'da_gan'
            don_hang.ngay_gan = datetime.utcnow()
            db.session.commit()
            
            flash('✅ Đã gán tài xế!', 'success')
            return redirect(url_for('admin.order_detail', id=id))
    
    tai_xes = TaiXe.query.filter_by(status='approved').all()
    return render_template('admin/assign_driver.html', don_hang=don_hang, tai_xes=tai_xes)

@bp.route('/orders/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_order(id):
    """Hủy đơn hàng"""
    if current_user.vai_tro != 'admin':
        return redirect(url_for('auth.login'))
    
    don_hang = DonHang.query.get_or_404(id)
    don_hang.trang_thai = 'da_huy'
    don_hang.ngay_huy = datetime.utcnow()
    don_hang.ghi_chu = request.form.get('ly_do', 'Hủy bởi admin')
    db.session.commit()
    
    flash('❌ Đã hủy đơn hàng!', 'warning')
    return redirect(url_for('admin.order_detail', id=id))

@bp.route('/drivers')
@login_required
def drivers():
    """Quản lý tài xế"""
    if current_user.vai_tro != 'admin':
        flash('❌ Bạn không có quyền!', 'error')
        return redirect(url_for('auth.login'))
    
    tai_xes = TaiXe.query.all()
    return render_template('admin/drivers.html', tai_xes=tai_xes)

@bp.route('/drivers/<int:id>/approve', methods=['POST'])
@login_required
def approve_driver(id):
    """Duyệt tài xế"""
    if current_user.vai_tro != 'admin':
        return redirect(url_for('auth.login'))
    
    tai_xe = TaiXe.query.get_or_404(id)
    tai_xe.status = 'approved'
    db.session.commit()
    
    flash('✅ Đã duyệt tài xế!', 'success')
    return redirect(url_for('admin.drivers'))

@bp.route('/drivers/<int:id>/reject', methods=['POST'])
@login_required
def reject_driver(id):
    """Từ chối tài xế"""
    if current_user.vai_tro != 'admin':
        return redirect(url_for('auth.login'))
    
    tai_xe = TaiXe.query.get_or_404(id)
    tai_xe.status = 'rejected'
    db.session.commit()
    
    flash('❌ Đã từ chối tài xế!', 'warning')
    return redirect(url_for('admin.drivers'))