from functools import wraps
from flask import flash, redirect, url_for, session
from flask_login import current_user

def login_required(f):
    """Yêu cầu đăng nhập"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('⚠️ Vui lòng đăng nhập để tiếp tục', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Yêu cầu quyền admin"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('❌ Bạn không có quyền truy cập trang này', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def customer_required(f):
    """Yêu cầu quyền customer"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_customer():
            flash('❌ Bạn không có quyền truy cập trang này', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def driver_required(f):
    """Yêu cầu quyền driver"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_driver():
            flash('❌ Bạn không có quyền truy cập trang này', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function