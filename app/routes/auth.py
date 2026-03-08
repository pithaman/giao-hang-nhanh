from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User, KhachHang, TaiXe
from werkzeug.security import generate_password_hash
from datetime import datetime

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Đăng nhập chung cho tất cả users"""
    if 'user_id' in session:
        flash('ℹ️ Bạn đã đăng nhập', 'info')
        return redirect(url_for('auth.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Tìm user
        user = User.query.filter_by(email=email).first()
        
        # ← QUAN TRỌNG: Kiểm tra user tồn tại VÀ password đúng
        if user and user.check_password(password):
            # Lưu session
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_role'] = user.vai_tro
            
            flash(f'✅ Đăng nhập thành công!', 'success')
            
            # Redirect theo role
            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            elif user.is_customer():
                return redirect(url_for('customer.home'))
            elif user.is_driver():
                return redirect(url_for('driver.home'))
        else:
            flash('❌ Email hoặc mật khẩu không đúng', 'danger')
    
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Đăng ký tài khoản customer mới"""
    if 'user_id' in session:
        return redirect(url_for('auth.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        ho_ten = request.form.get('ho_ten')
        so_dien_thoai = request.form.get('so_dien_thoai')
        
        # Validation
        if not email or not password:
            flash('❌ Vui lòng điền đầy đủ thông tin', 'danger')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('❌ Mật khẩu xác nhận không khớp', 'danger')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('❌ Mật khẩu phải có ít nhất 6 ký tự', 'danger')
            return render_template('auth/register.html')
        
        # Kiểm tra email đã tồn tại
        if User.query.filter_by(email=email).first():
            flash('❌ Email đã được đăng ký', 'danger')
            return render_template('auth/register.html')
        
        try:
            # Tạo user mới
            user = User(
                email=email,
                mat_khau='',  # Sẽ hash ở dòng dưới
                vai_tro='khach_hang'
            )
            user.set_password(password)  # Hash password
            
            db.session.add(user)
            db.session.flush()
            
            # Tạo customer record
            customer = KhachHang(
                nguoi_dung_id=user.id,
                ho_ten=ho_ten,
                so_dien_thoai=so_dien_thoai,
                dia_chi=''
            )
            db.session.add(customer)
            db.session.commit()
            
            flash('✅ Đăng ký thành công! Vui lòng đăng nhập', 'success')
            return redirect(url_for('auth.login'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Lỗi khi đăng ký: {str(e)}', 'danger')
    
    return render_template('auth/register.html')

@bp.route('/logout')
def logout():
    """Đăng xuất"""
    session.clear()
    flash('✅ Đã đăng xuất thành công', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
def dashboard():
    """Dashboard sau khi login"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    return render_template('auth/dashboard.html', user=user)

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """Hồ sơ người dùng"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        # Cập nhật thông tin
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        
        if current_password and new_password:
            if user.check_password(current_password):
                user.set_password(new_password)
                db.session.commit()
                flash('✅ Đã cập nhật mật khẩu thành công', 'success')
            else:
                flash('❌ Mật khẩu hiện tại không đúng', 'danger')
        
        # Cập nhật thông tin customer
        if user.is_customer() and user.khach_hang:
            user.khach_hang.ho_ten = request.form.get('ho_ten', user.khach_hang.ho_ten)
            user.khach_hang.so_dien_thoai = request.form.get('so_dien_thoai', user.khach_hang.so_dien_thoai)
            user.khach_hang.dia_chi = request.form.get('dia_chi', user.khach_hang.dia_chi)
            db.session.commit()
        
        flash('✅ Cập nhật hồ sơ thành công', 'success')
    
    return render_template('auth/profile.html', user=user)