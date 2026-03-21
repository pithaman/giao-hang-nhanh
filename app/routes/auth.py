# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('✅ Đăng nhập thành công!', 'success')
            
            # ✅ QUAN TRỌNG: Dùng .lower() để so sánh không phân biệt hoa thường
            role = (user.vai_tro or 'customer').lower().strip()
            
            next_page = request.args.get('next')
            
            if role == 'admin':
                return redirect(next_page or url_for('admin.dashboard'))
            elif role == 'customer':
                return redirect(next_page or url_for('customer.dashboard'))
            elif role == 'driver':
                return redirect(next_page or url_for('driver.dashboard'))
            else:
                # Fallback: về dashboard theo role mặc định
                return redirect(url_for('auth.login'))
        else:
            flash('❌ Email hoặc mật khẩu không đúng!', 'error')
    
    # Nếu đã login rồi, redirect theo role
    if current_user.is_authenticated:
        role = (current_user.vai_tro or 'customer').lower().strip()
        if role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif role == 'customer':
            return redirect(url_for('customer.dashboard'))
        elif role == 'driver':
            return redirect(url_for('driver.dashboard'))
    
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        phone = request.form.get('phone')
        vai_tro = request.form.get('vai_tro', 'customer')
        
        if User.query.filter_by(email=email).first():
            flash('❌ Email đã tồn tại!', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(email=email, name=name, phone=phone, vai_tro=vai_tro)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('✅ Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('✅ Đã đăng xuất!', 'info')
    return redirect(url_for('auth.login'))