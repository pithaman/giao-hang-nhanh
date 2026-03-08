from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Kiểm tra admin đã tồn tại chưa
    admin = User.query.filter_by(email='admin@giaohang.com').first()
    
    if not admin:
        admin = User(
            email='admin@giaohang.com',
            mat_khau='',
            vai_tro='admin'
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Đã tạo tài khoản admin thành công!")
        print("   Email: admin@giaohang.com")
        print("   Password: admin123")
    else:
        print("ℹ️ Tài khoản admin đã tồn tại")