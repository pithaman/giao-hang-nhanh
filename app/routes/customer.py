# app/routes/customer.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import DonHang
from datetime import datetime

bp = Blueprint('customer', __name__)

@bp.route('/')
@login_required
def dashboard():
    if current_user.vai_tro != 'customer':
        return redirect(url_for('auth.login'))
    
    don_hangs = DonHang.query.filter_by(customer_id=current_user.id).order_by(DonHang.ngay_tao.desc()).limit(5).all()
    return render_template('customer/dashboard.html', don_hangs=don_hangs)

@bp.route('/place-order', methods=['GET', 'POST'])
@login_required
def place_order():
    if current_user.vai_tro != 'customer':
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        don_hang = DonHang(
            customer_id=current_user.id,
            dia_chi_lay=request.form.get('dia_chi_lay'),
            dia_chi_giao=request.form.get('dia_chi_giao'),
            loai_hang=request.form.get('loai_hang'),
            can_nang=float(request.form.get('can_nang', 1)),
            ghi_chu=request.form.get('ghi_chu'),
            service_type=request.form.get('service_type', 'hoa_toc'),
            gia_tien=float(request.form.get('gia_tien', 35000)),
            phi_dich_vu=0,
            giam_gia=0,
            tong_tien=float(request.form.get('gia_tien', 35000)),
            trang_thai='cho_duyet',
            ngay_tao=datetime.utcnow()
        )
        
        # ✅ Commit TRƯỚC để có id (nếu cần)
        db.session.add(don_hang)
        db.session.commit()  # ← Commit để save vào DB
        
        # ✅ Tạo ma_don SAU khi có object
        don_hang.ma_don = don_hang.generate_ma_don()
        db.session.commit()  # ← Commit lại để lưu ma_don
        
        flash('✅ Đặt hàng thành công!', 'success')
        return redirect(url_for('customer.my_orders'))
    
    return render_template('customer/place_order.html')

@bp.route('/my-orders')
@login_required
def my_orders():
    if current_user.vai_tro != 'customer':
        return redirect(url_for('auth.login'))
    
    don_hangs = DonHang.query.filter_by(customer_id=current_user.id).order_by(DonHang.ngay_tao.desc()).all()
    return render_template('customer/my_orders.html', don_hangs=don_hangs)

# Thêm vào cuối file
@bp.route('/orders/<int:id>')
@login_required
def order_detail(id):
    if current_user.vai_tro != 'customer':
        return redirect(url_for('auth.login'))
    
    don_hang = DonHang.query.get_or_404(id)
    if don_hang.customer_id != current_user.id:
        flash('❌ Bạn không có quyền xem đơn này!', 'error')
        return redirect(url_for('customer.my_orders'))
    
    return render_template('customer/order_detail.html', don_hang=don_hang)

@bp.route('/orders/<int:id>/track')
@login_required
def track_order(id):
    if current_user.vai_tro != 'customer':
        return redirect(url_for('auth.login'))
    
    don_hang = DonHang.query.get_or_404(id)
    if don_hang.customer_id != current_user.id:
        flash('❌ Bạn không có quyền!', 'error')
        return redirect(url_for('customer.my_orders'))
    
    return render_template('customer/track_order.html', don_hang=don_hang)

@bp.route('/orders/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_order(id):
    if current_user.vai_tro != 'customer':
        return redirect(url_for('auth.login'))
    
    don_hang = DonHang.query.get_or_404(id)
    if don_hang.customer_id != current_user.id:
        flash('❌ Bạn không có quyền hủy đơn này!', 'error')
        return redirect(url_for('customer.my_orders'))
    
    if don_hang.trang_thai not in ['cho_duyet', 'da_duyet']:
        flash('❌ Không thể hủy đơn đã giao cho tài xế!', 'error')
        return redirect(url_for('customer.order_detail', id=id))
    
    don_hang.trang_thai = 'da_huy'
    don_hang.ngay_huy = datetime.utcnow()
    db.session.commit()
    
    flash('✅ Đã hủy đơn hàng!', 'success')
    return redirect(url_for('customer.my_orders'))