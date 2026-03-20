# app/routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import DonHang, TaiXe, User

bp = Blueprint('admin', __name__)

@bp.route('/')
@login_required
def dashboard():
    if current_user.vai_tro != 'admin':
        flash('❌ Bạn không có quyền!', 'error')
        return redirect(url_for('auth.login'))
    
    tong_don = DonHang.query.count()
    don_cho_duyet = DonHang.query.filter_by(trang_thai='cho_duyet').count()
    don_hoan_thanh = DonHang.query.filter_by(trang_thai='hoan_thanh').count()
    tai_xe_pending = TaiXe.query.filter_by(status='pending').count()
    
    return render_template('admin/dashboard.html',
                          tong_don=tong_don,
                          don_cho_duyet=don_cho_duyet,
                          don_hoan_thanh=don_hoan_thanh,
                          tai_xe_pending=tai_xe_pending)

@bp.route('/orders')
@login_required
def orders():
    if current_user.vai_tro != 'admin':
        flash('❌ Bạn không có quyền!', 'error')
        return redirect(url_for('auth.login'))
    
    don_hangs = DonHang.query.order_by(DonHang.ngay_tao.desc()).all()
    return render_template('admin/orders.html', don_hangs=don_hangs)

@bp.route('/drivers')
@login_required
def drivers():
    if current_user.vai_tro != 'admin':
        flash('❌ Bạn không có quyền!', 'error')
        return redirect(url_for('auth.login'))
    
    tai_xes = TaiXe.query.all()
    return render_template('admin/drivers.html', tai_xes=tai_xes)

@bp.route('/drivers/<int:id>/approve', methods=['POST'])
@login_required
def approve_driver(id):
    if current_user.vai_tro != 'admin':
        return redirect(url_for('auth.login'))
    
    tai_xe = TaiXe.query.get_or_404(id)
    tai_xe.status = 'approved'
    db.session.commit()
    flash('✅ Đã duyệt tài xế!', 'success')
    return redirect(url_for('admin.drivers'))

# Thêm vào cuối file app/routes/admin.py

@bp.route('/orders/<int:id>')
@login_required
def order_detail(id):
    if current_user.vai_tro != 'admin':
        return redirect(url_for('auth.login'))
    
    don_hang = DonHang.query.get_or_404(id)
    return render_template('admin/order_detail.html', don_hang=don_hang)

@bp.route('/orders/<int:id>/approve', methods=['POST'])
@login_required
def approve_order(id):
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
    if current_user.vai_tro != 'admin':
        return redirect(url_for('auth.login'))
    
    don_hang = DonHang.query.get_or_404(id)
    don_hang.trang_thai = 'da_huy'
    don_hang.ngay_huy = datetime.utcnow()
    db.session.commit()
    
    flash('❌ Đã hủy đơn hàng!', 'warning')
    return redirect(url_for('admin.order_detail', id=id))