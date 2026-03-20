# app/routes/driver.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

bp = Blueprint('driver', __name__)

@bp.route('/')
@login_required
def dashboard():
    if current_user.vai_tro != 'driver':
        return redirect(url_for('auth.login'))
    return render_template('driver/dashboard.html')