from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User, DonHang, KhachHang, TaiXe
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta

bp = Blueprint('api', __name__, url_prefix='/api')

# ============================================
# AUTHENTICATION APIs
# ============================================
@bp.route('/login', methods=['POST'])
def api_login():
    """API Login - Returns JWT token"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):
        # Create token with user info
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(hours=1),
            additional_claims={
                'email': user.email,
                'role': user.vai_tro
            }
        )
        
        return jsonify({
            'success': True,
            'message': 'Đăng nhập thành công',
            'data': {
                'access_token': access_token,
                'token_type': 'Bearer',
                'expires_in': 3600,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'role': user.vai_tro,
                    'name': user.khach_hang.ho_ten if user.khach_hang else (
                        user.tai_xe.ho_ten if user.tai_xe else user.email
                    )
                }
            }
        }), 200
    
    return jsonify({
        'success': False,
        'message': 'Email hoặc mật khẩu không đúng'
    }), 401

@bp.route('/register', methods=['POST'])
def api_register():
    """API Register - Create new customer"""
    data = request.get_json()
    
    # Validation
    if not data.get('email') or not data.get('password'):
        return jsonify({'success': False, 'message': 'Thiếu thông tin'}), 400
    
    # Check if email exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'message': 'Email đã tồn tại'}), 400
    
    try:
        # Create user
        user = User(
            email=data['email'],
            mat_khau='',
            vai_tro='khach_hang'
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.flush()
        
        # Create customer
        customer = KhachHang(
            nguoi_dung_id=user.id,
            ho_ten=data.get('ho_ten', ''),
            so_dien_thoai=data.get('so_dien_thoai', ''),
            dia_chi=data.get('dia_chi', '')
        )
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Đăng ký thành công'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# ============================================
# ORDER APIs
# ============================================
@bp.route('/orders', methods=['GET'])
@jwt_required()
def api_get_orders():
    """Get all orders (with filters)"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', '')
    
    query = DonHang.query
    
    # Filter by user role
    if user.is_customer():
        query = query.filter_by(khach_hang_id=user.khach_hang.id)
    elif user.is_driver():
        query = query.filter_by(tai_xe_id=user.tai_xe.id)
    
    if status:
        query = query.filter_by(trang_thai=status)
    
    query = query.order_by(DonHang.ngay_tao.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    orders = []
    for dh in pagination.items:
        orders.append({
            'id': dh.id,
            'ma_don': dh.ma_don,
            'khach_hang': dh.khach_hang.ho_ten if dh.khach_hang else 'N/A',
            'dia_chi_giao': dh.dia_chi_giao,
            'tai_xe': dh.tai_xe.ho_ten if dh.tai_xe else 'Chưa gán',
            'trang_thai': dh.trang_thai,
            'tong_tien': float(dh.tong_tien),
            'ngay_tao': dh.ngay_tao.isoformat()
        })
    
    return jsonify({
        'success': True,
        'data': {
            'orders': orders,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }
    }), 200

@bp.route('/orders', methods=['POST'])
@jwt_required()
def api_create_order():
    """Create new order"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_customer():
        return jsonify({'success': False, 'message': 'Chỉ khách hàng mới tạo được đơn'}), 403
    
    data = request.get_json()
    
    try:
        ma_don = 'DH' + datetime.now().strftime('%Y%m%d%H%M%S')
        
        order = DonHang(
            khach_hang_id=user.khach_hang.id,
            ma_don=ma_don,
            dia_chi_lay=data.get('dia_chi_lay'),
            dia_chi_giao=data.get('dia_chi_giao'),
            phi_van_chuyen=data.get('phi_van_chuyen', 30000),
            tien_hang=0,
            tien_giam_gia=0,
            tong_tien=data.get('phi_van_chuyen', 30000),
            ghi_chu=data.get('ghi_chu', ''),
            trang_thai='cho_duyet'
        )
        
        db.session.add(order)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tạo đơn thành công',
            'data': {
                'ma_don': order.ma_don,
                'id': order.id
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def api_get_order_detail(order_id):
    """Get order detail"""
    order = DonHang.query.get_or_404(order_id)
    
    return jsonify({
        'success': True,
        'data': {
            'id': order.id,
            'ma_don': order.ma_don,
            'khach_hang': order.khach_hang.ho_ten if order.khach_hang else 'N/A',
            'dia_chi_lay': order.dia_chi_lay,
            'dia_chi_giao': order.dia_chi_giao,
            'tai_xe': order.tai_xe.ho_ten if order.tai_xe else 'Chưa gán',
            'trang_thai': order.trang_thai,
            'phi_van_chuyen': float(order.phi_van_chuyen),
            'tong_tien': float(order.tong_tien),
            'ngay_tao': order.ngay_tao.isoformat()
        }
    }), 200

# ============================================
# PROFILE APIs
# ============================================
@bp.route('/profile', methods=['GET'])
@jwt_required()
def api_get_profile():
    """Get current user profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    return jsonify({
        'success': True,
        'data': {
            'id': user.id,
            'email': user.email,
            'role': user.vai_tro,
            'ho_ten': user.khach_hang.ho_ten if user.khach_hang else (
                user.tai_xe.ho_ten if user.tai_xe else ''
            ),
            'so_dien_thoai': user.khach_hang.so_dien_thoai if user.khach_hang else (
                user.tai_xe.so_dien_thoai if user.tai_xe else ''
            )
        }
    }), 200