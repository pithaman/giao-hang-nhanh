# app/routes/customer.py
from app.services.email_service import send_order_confirmation_email
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models import DonHang
from datetime import datetime
import random

bp = Blueprint('customer', __name__)

@bp.route('/')
@login_required
def dashboard():
    """Customer dashboard"""
    if current_user.vai_tro != 'customer':
        flash('❌ Bạn không có quyền truy cập!', 'error')
        return redirect(url_for('auth.login'))
    
    # Lấy 5 đơn hàng gần nhất của customer
    don_hangs = DonHang.query.filter_by(customer_id=current_user.id)\
        .order_by(DonHang.ngay_tao.desc()).limit(5).all()
    
    return render_template('customer/dashboard.html', don_hangs=don_hangs)

@bp.route('/place-order', methods=['GET', 'POST'])
@login_required
def place_order():
    """Đặt hàng mới"""
    if current_user.vai_tro != 'customer':
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        dia_chi_lay = request.form.get('dia_chi_lay')
        dia_chi_giao = request.form.get('dia_chi_giao')
        loai_hang = request.form.get('loai_hang')
        can_nang = float(request.form.get('can_nang', 1))
        ghi_chu = request.form.get('ghi_chu', '')
        service_type = request.form.get('service_type', 'hoa_toc')
        gia_tien = float(request.form.get('gia_tien', 35000))
        
        # Tạo đơn hàng
        don_hang = DonHang(
            customer_id=current_user.id,
            dia_chi_lay=dia_chi_lay,
            dia_chi_giao=dia_chi_giao,
            loai_hang=loai_hang,
            can_nang=can_nang,
            ghi_chu=ghi_chu,
            service_type=service_type,
            gia_tien=gia_tien,
            phi_dich_vu=0,
            giam_gia=0,
            tong_tien=gia_tien,
            trang_thai='cho_duyet',
            ngay_tao=datetime.utcnow()
        )
        
        # Generate mã đơn
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_num = random.randint(1000, 9999)
        don_hang.ma_don = f'DH{timestamp}{random_num}'
        
        db.session.add(don_hang)
        db.session.commit()

        try:
            send_order_confirmation_email(don_hang)
            print(f"✅ SendGrid email sent to {don_hang.customer.email}")
        except Exception as e:
            print(f"⚠️ Email failed: {e}")

        flash('✅ Đặt hàng thành công! Email xác nhận đã được gửi!', 'success')
        return redirect(url_for('customer.order_detail', id=don_hang.id))

        
        flash('✅ Đặt hàng thành công! Mã đơn: ' + don_hang.ma_don, 'success')
        return redirect(url_for('customer.order_detail', id=don_hang.id))
    
    return render_template('customer/place_order.html')

@bp.route('/my-orders')
@login_required
def my_orders():
    """Xem lịch sử đơn hàng"""
    if current_user.vai_tro != 'customer':
        return redirect(url_for('auth.login'))
    
    don_hangs = DonHang.query.filter_by(customer_id=current_user.id)\
        .order_by(DonHang.ngay_tao.desc()).all()
    
    return render_template('customer/my_orders.html', don_hangs=don_hangs)

@bp.route('/order/<int:id>')
@login_required
def order_detail(id):
    """Chi tiết đơn hàng"""
    if current_user.vai_tro != 'customer':
        return redirect(url_for('auth.login'))
    
    don_hang = DonHang.query.get_or_404(id)
    
    # Check xem đơn này có thuộc về customer này không
    if don_hang.customer_id != current_user.id:
        flash('❌ Bạn không có quyền xem đơn này!', 'error')
        return redirect(url_for('customer.my_orders'))
    
    return render_template('customer/order_detail.html', don_hang=don_hang)

@bp.route('/track/<ma_don>')
def track_order(ma_don):
    """Theo dõi đơn hàng theo mã (public - không cần login)"""
    don_hang = DonHang.query.filter_by(ma_don=ma_don).first_or_404()
    return render_template('customer/track_order.html', don_hang=don_hang)

@bp.route('/api/orders', methods=['POST'])
@login_required
def api_create_order():
    """API endpoint để tạo đơn hàng (cho mobile app)"""
    if current_user.vai_tro != 'customer':
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    don_hang = DonHang(
        customer_id=current_user.id,
        dia_chi_lay=data.get('dia_chi_lay'),
        dia_chi_giao=data.get('dia_chi_giao'),
        loai_hang=data.get('loai_hang'),
        can_nang=float(data.get('can_nang', 1)),
        ghi_chu=data.get('ghi_chu', ''),
        service_type=data.get('service_type', 'hoa_toc'),
        gia_tien=float(data.get('gia_tien', 35000)),
        phi_dich_vu=0,
        giam_gia=0,
        tong_tien=float(data.get('gia_tien', 35000)),
        trang_thai='cho_duyet',
        ngay_tao=datetime.utcnow()
    )
    
    # Generate mã đơn
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_num = random.randint(1000, 9999)
    don_hang.ma_don = f'DH{timestamp}{random_num}'
    
    db.session.add(don_hang)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'ma_don': don_hang.ma_don,
        'id': don_hang.id
    }), 201