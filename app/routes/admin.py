# app/routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from app.extensions import db
from app.models import DonHang, TaiXe, User
from datetime import datetime, timedelta
from sqlalchemy import func
import pandas as pd
import io

bp = Blueprint('admin', __name__)

# ========================================
# DASHBOARD ROUTE
# ========================================
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
    don_da_duyet = DonHang.query.filter_by(trang_thai='da_duyet').count()
    don_dang_giao = DonHang.query.filter_by(trang_thai='dang_giao').count()
    don_hoan_thanh = DonHang.query.filter_by(trang_thai='hoan_thanh').count()
    don_da_huy = DonHang.query.filter_by(trang_thai='da_huy').count()
    
    # === ĐƠN THEO NGÀY (7 NGÀY GẦN NHẤT) - CHO CHART ===
    ngay_gan_nhat = datetime.utcnow() - timedelta(days=7)
    don_theo_ngay_query = db.session.query(
        func.date(DonHang.ngay_tao).label('ngay'),
        func.count(DonHang.id).label('so_don'),
        func.sum(DonHang.tong_tien).label('doanh_thu')
    ).filter(
        DonHang.ngay_tao >= ngay_gan_nhat
    ).group_by(func.date(DonHang.ngay_tao)).order_by(func.date(DonHang.ngay_tao)).all()
    
    # Format data cho Chart.js
    don_theo_ngay_labels = []
    don_theo_ngay_so_don = []
    don_theo_ngay_doanh_thu = []
    
    for item in don_theo_ngay_query:
        don_theo_ngay_labels.append(item.ngay.strftime('%d/%m'))
        don_theo_ngay_so_don.append(item.so_don)
        don_theo_ngay_doanh_thu.append(item.doanh_thu or 0)
    
    # === TOP TÀI XẾ HIỆU SUẤT ===
    top_tai_xe = db.session.query(
        TaiXe.id,
        User.name,
        func.count(DonHang.id).label('tong_don'),
        TaiXe.rating
    ).join(User, TaiXe.user_id == User.id
    ).outerjoin(DonHang, DonHang.tai_xe_id == TaiXe.id
    ).group_by(TaiXe.id, User.name, TaiXe.rating
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
        don_da_duyet=don_da_duyet,
        don_dang_giao=don_dang_giao,
        don_hoan_thanh=don_hoan_thanh,
        don_da_huy=don_da_huy,
        don_theo_ngay_labels=don_theo_ngay_labels,
        don_theo_ngay_so_don=don_theo_ngay_so_don,
        don_theo_ngay_doanh_thu=don_theo_ngay_doanh_thu,
        top_tai_xe=top_tai_xe,
        don_moi_nhat=don_moi_nhat
    )

# ========================================
# ORDERS ROUTES
# ========================================
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

# ========================================
# DRIVERS ROUTES
# ========================================
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

# ========================================
# REPORTS ROUTES (EXCEL EXPORT) - FIX LỖI THIẾU ROUTE
# ========================================

# ✅ THÊM ROUTE NÀY ĐỂ TRUY CẬP TRANG CHỌN NGÀY
@bp.route('/reports')
@login_required
def reports():
    """Trang báo cáo - Hiển thị form để người dùng chọn filter"""
    if current_user.vai_tro != 'admin':
        flash('❌ Bạn không có quyền!', 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('admin/reports.html')


@bp.route('/reports/export', methods=['POST'])
@login_required
def export_excel():
    """Export đơn hàng ra file Excel"""
    if current_user.vai_tro != 'admin':
        return redirect(url_for('auth.login'))
    
    # ✅ LẤY TẤT CẢ FORM DATA
    print("\n" + "="*60)
    print("🔍 FORM DATA DEBUG:")
    print(f"   request.form: {request.form.to_dict()}")
    
    date_from = request.form.get('date_from', '').strip()
    date_to = request.form.get('date_to', '').strip()
    status = request.form.get('status', '').strip()
    customer_id = request.form.get('customer_id', '').strip()
    
    print("\n🔍 FILTER VALUES:")
    print(f"   date_from: '{date_from}' (type: {type(date_from)})")
    print(f"   date_to: '{date_to}' (type: {type(date_to)})")
    print(f"   status: '{status}' (type: {type(status)})")
    print(f"   customer_id: '{customer_id}' (type: {type(customer_id)})")
    
    # Build query
    query = DonHang.query
    
    # ✅ DATE FILTER
    if date_from:
        try:
            query = query.filter(DonHang.ngay_tao >= datetime.strptime(date_from, '%Y-%m-%d'))
            print(f"\n✅ Applied date_from filter: {date_from}")
        except Exception as e:
            print(f"\n⚠️ Invalid date_from: {e}")
    
    if date_to:
        try:
            query = query.filter(DonHang.ngay_tao <= datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1))
            print(f"✅ Applied date_to filter: {date_to}")
        except Exception as e:
            print(f"⚠️ Invalid date_to: {e}")
    
    # ✅ STATUS FILTER
    if status and status != 'all':
        query = query.filter(DonHang.trang_thai == status)
        print(f"✅ Applied status filter: {status}")
    else:
        print(f"⚠️ NOT applying status filter (value: '{status}')")
    
    # ✅ CUSTOMER FILTER - QUAN TRỌNG NHẤT
    print(f"\n🔍 CUSTOMER ID CHECK:")
    print(f"   customer_id value: '{customer_id}'")
    print(f"   customer_id != '': {customer_id != ''}")
    print(f"   customer_id != '0': {customer_id != '0'}")
    print(f"   bool(customer_id): {bool(customer_id)}")
    
    if customer_id and customer_id != '0' and customer_id != '':
        try:
            cust_id = int(customer_id)
            print(f"\n✅ Filtering customer_id = {cust_id}")
            query = query.filter(DonHang.customer_id == cust_id)
            
            # Test query (Chỉ chạy all() để debug, không dùng result này cho file excel)
            test_results = query.all()
            print(f"✅ Query returned {len(test_results)} orders for customer_id {cust_id}")
            for order in test_results:
                print(f"   - Order {order.id}: {order.customer.name if order.customer else 'NULL'}")
            
            # Build lại query để sắp xếp và lấy data cuối cùng
            query = DonHang.query
            if date_from: query = query.filter(DonHang.ngay_tao >= datetime.strptime(date_from, '%Y-%m-%d'))
            if date_to: query = query.filter(DonHang.ngay_tao <= datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1))
            if status and status != 'all': query = query.filter(DonHang.trang_thai == status)
            if customer_id and customer_id != '0' and customer_id != '': query = query.filter(DonHang.customer_id == cust_id)
            
            don_hangs = query.order_by(DonHang.ngay_tao.desc()).all()
            
        except Exception as e:
            print(f"\n⚠️ Invalid customer_id: {e}")
            don_hangs = query.order_by(DonHang.ngay_tao.desc()).all()
    else:
        print("\n⚠️ NOT filtering customer_id (empty or 0) - Will get ALL customers")
        don_hangs = query.order_by(DonHang.ngay_tao.desc()).all()
    
    print(f"\n📊 FINAL RESULT: {len(don_hangs)} orders")
    print("="*60 + "\n")
    
    # Convert to list of dicts
    data = []
    for don in don_hangs:
        data.append({
            'Mã đơn': don.ma_don or f'#{don.id}',
            'Khách hàng': don.customer.name if don.customer else 'NULL',
            'Email': don.customer.email if don.customer else 'NULL',
            'SĐT': don.customer.phone if don.customer else 'NULL',
            'Địa chỉ lấy': don.dia_chi_lay,
            'Địa chỉ giao': don.dia_chi_giao,
            'Loại hàng': don.loai_hang or 'N/A',
            'Cân nặng (kg)': don.can_nang,
            'Dịch vụ': 'Hỏa tốc' if don.service_type == 'hoa_toc' else 'Trong ngày',
            'Giá cơ bản': don.gia_tien,
            'Phí dịch vụ': don.phi_dich_vu,
            'Giảm giá': don.giam_gia,
            'Tổng tiền': don.tong_tien,
            'Trạng thái': don.trang_thai,
            'Ngày tạo': don.ngay_tao.strftime('%d/%m/%Y %H:%M'),
            'Ngày duyệt': don.ngay_duyet.strftime('%d/%m/%Y %H:%M') if don.ngay_duyet else '',
            'Tài xế': don.tai_xe.user.name if don.tai_xe else 'Chưa gán',
        })
    
    # Create Excel
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='DonHang')
        worksheet = writer.sheets['DonHang']
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    output.seek(0)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'BaoCao_DonHang_{timestamp}.xlsx'
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )


@bp.route('/reports/export-summary', methods=['POST'])
@login_required
def export_summary():
    """Export báo cáo tổng hợp (thống kê)"""
    if current_user.vai_tro != 'admin':
        return redirect(url_for('auth.login'))
    
    # Lấy filter
    date_from = request.form.get('date_from', '').strip()
    date_to = request.form.get('date_to', '').strip()
    
    # Build query
    query = DonHang.query
    if date_from:
        query = query.filter(DonHang.ngay_tao >= datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        query = query.filter(DonHang.ngay_tao <= datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1))
    
    don_hangs = query.all()
    
    # Tính thống kê
    stats = {
        'Tổng số đơn': len(don_hangs),
        'Tổng doanh thu': sum(d.tong_tien for d in don_hangs),
        'Đơn hoàn thành': len([d for d in don_hangs if d.trang_thai == 'hoan_thanh']),
        'Đơn đang giao': len([d for d in don_hangs if d.trang_thai == 'dang_giao']),
        'Đơn chờ duyệt': len([d for d in don_hangs if d.trang_thai == 'cho_duyet']),
        'Đơn đã hủy': len([d for d in don_hangs if d.trang_thai == 'da_huy']),
        'Khách hàng duy nhất': len(set(d.customer_id for d in don_hangs)),
        'Tài xế tham gia': len(set(d.tai_xe_id for d in don_hangs if d.tai_xe_id)),
    }
    
    # Tạo DataFrame thống kê
    summary_data = [
        {'Metric': k, 'Value': f'{v:,.0f}đ' if 'doanh thu' in k.lower() else v}
        for k, v in stats.items()
    ]
    df = pd.DataFrame(summary_data)
    
    # Thêm chi tiết theo trạng thái
    status_stats = []
    for trang_thai in ['cho_duyet', 'da_duyet', 'dang_giao', 'hoan_thanh', 'da_huy']:
        count = len([d for d in don_hangs if d.trang_thai == trang_thai])
        total = sum(d.tong_tien for d in don_hangs if d.trang_thai == trang_thai)
        status_stats.append({
            'Trạng thái': trang_thai,
            'Số đơn': count,
            'Doanh thu': f'{total:,.0f}đ'
        })
    df_status = pd.DataFrame(status_stats)
    
    # Create Excel with multiple sheets
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='TongQuan')
        df_status.to_excel(writer, index=False, sheet_name='TheoTrangThai')
    
    output.seek(0)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'BaoCao_TongHop_{timestamp}.xlsx'
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )