from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import DonHang, KhachHang, TaiXe, User
from sqlalchemy import func
from datetime import datetime
from flask import send_file
import io
from openpyxl import Workbook

bp = Blueprint('admin', __name__)

@bp.route('/')
def dashboard():
    # Lấy dữ liệu từ database
    tong_don_hang = DonHang.query.count()
    tong_tai_xe = TaiXe.query.filter_by(trang_thai='hoat_dong').count()
    
    # Tính doanh thu (tổng tiền từ các đơn hoàn thành)
    doanh_thu = db.session.query(func.sum(DonHang.tong_tien)).filter(
        DonHang.trang_thai == 'hoan_thanh'
    ).scalar() or 0
    
    # Lấy 5 đơn hàng gần nhất
    don_hang_gan_day = DonHang.query.order_by(DonHang.ngay_tao.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                           tong_don=tong_don_hang,
                           tong_tai_xe=tong_tai_xe,
                           doanh_thu=doanh_thu,
                           don_hangs=don_hang_gan_day)

@bp.route('/orders')
def orders():
    """Hiển thị tất cả đơn hàng với pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    # Base query
    query = DonHang.query.order_by(DonHang.ngay_tao.desc())
    
    # Filter by search
    if search:
        query = query.filter(
            db.or_(
                DonHang.ma_don.like(f'%{search}%'),
                DonHang.dia_chi_giao.like(f'%{search}%')
            )
        )
    
    # Filter by status
    if status:
        query = query.filter(DonHang.trang_thai == status)
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    don_hangs = pagination.items
    
    return render_template('admin/orders.html', 
                           don_hangs=don_hangs,
                           pagination=pagination,
                           search=search,
                           status=status)

@bp.route('/order/<int:id>')
def order_detail(id):
    """Chi tiết đơn hàng"""
    don_hang = DonHang.query.get_or_404(id)
    return render_template('admin/order_detail.html', don_hang=don_hang)

@bp.route('/order/create', methods=['GET', 'POST'])
def create_order():
    """Tạo đơn hàng mới"""
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        khach_hang_id = request.form.get('khach_hang_id')
        tai_xe_id = request.form.get('tai_xe_id') or None
        dia_chi_lay = request.form.get('dia_chi_lay')
        dia_chi_giao = request.form.get('dia_chi_giao')
        phi_van_chuyen = request.form.get('phi_van_chuyen', 0)
        ghi_chu = request.form.get('ghi_chu', '')
        
        # Tạo mã đơn
        ma_don = 'DH' + datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Tạo đơn hàng
        don_hang = DonHang(
            khach_hang_id=khach_hang_id,
            tai_xe_id=tai_xe_id,
            ma_don=ma_don,
            dia_chi_lay=dia_chi_lay,
            dia_chi_giao=dia_chi_giao,
            phi_van_chuyen=phi_van_chuyen,
            tien_hang=0,
            tien_giam_gia=0,
            tong_tien=phi_van_chuyen,
            ghi_chu=ghi_chu,
            trang_thai='cho_duyet'
        )
        
        try:
            db.session.add(don_hang)
            db.session.commit()
            flash('✅ Tạo đơn hàng thành công!', 'success')
            return redirect(url_for('admin.orders'))
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Lỗi khi tạo đơn: {str(e)}', 'danger')
    
    # GET request - hiển thị form
    khach_hangs = KhachHang.query.all()
    tai_xes = TaiXe.query.filter_by(trang_thai='hoat_dong').all()
    return render_template('admin/order_form.html', 
                           don_hang=None,
                           khach_hangs=khach_hangs,
                           tai_xes=tai_xes)

@bp.route('/order/<int:id>/edit', methods=['GET', 'POST'])
def edit_order(id):
    """Sửa đơn hàng"""
    don_hang = DonHang.query.get_or_404(id)
    
    if request.method == 'POST':
        don_hang.tai_xe_id = request.form.get('tai_xe_id') or None
        don_hang.trang_thai = request.form.get('trang_thai')
        don_hang.phi_van_chuyen = request.form.get('phi_van_chuyen', 0)
        don_hang.tong_tien = don_hang.phi_van_chuyen
        don_hang.ghi_chu = request.form.get('ghi_chu', '')
        
        # Cập nhật ngày gán nếu có tài xế
        if don_hang.tai_xe_id and not don_hang.ngay_gan:
            don_hang.ngay_gan = datetime.utcnow()
        
        # Cập nhật ngày hoàn thành
        if don_hang.trang_thai == 'hoan_thanh' and not don_hang.ngay_hoan_thanh:
            don_hang.ngay_hoan_thanh = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('✅ Cập nhật đơn hàng thành công!', 'success')
            return redirect(url_for('admin.orders'))
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Lỗi khi cập nhật: {str(e)}', 'danger')
    
    # GET request
    khach_hangs = KhachHang.query.all()
    tai_xes = TaiXe.query.filter_by(trang_thai='hoat_dong').all()
    return render_template('admin/order_form.html', 
                           don_hang=don_hang,
                           khach_hangs=khach_hangs,
                           tai_xes=tai_xes)

@bp.route('/orders/delete/<int:id>', methods=['POST'])
def delete_order(id):
    """Xóa đơn hàng"""
    don_hang = DonHang.query.get_or_404(id)
    
    try:
        ma_don = don_hang.ma_don
        db.session.delete(don_hang)
        db.session.commit()
        flash(f'✅ Đã xóa đơn hàng {ma_don}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Lỗi khi xóa: {str(e)}', 'danger')
    
    return redirect(url_for('admin.orders'))

@bp.route('/drivers')
def drivers():
    """Quản lý tài xế"""
    tai_xes = TaiXe.query.all()
    return render_template('admin/drivers.html', tai_xes=tai_xes)

@bp.route('/customers')
def customers():
    """Quản lý khách hàng"""
    khach_hangs = KhachHang.query.all()
    return render_template('admin/customers.html', khach_hangs=khach_hangs)

@bp.route('/orders/export')
def export_orders():
    """Export đơn hàng ra Excel"""
    # Lấy tất cả đơn hàng
    don_hangs = DonHang.query.order_by(DonHang.ngay_tao.desc()).all()
    # Download
    filename = f'DonHang_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )