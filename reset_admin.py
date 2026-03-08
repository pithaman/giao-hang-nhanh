from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Xóa admin cũ (nếu có)
    old_admin = User.query.filter_by(email='admin@giaohang.com').first()
    if old_admin:
        db.session.delete(old_admin)
        db.session.commit()
        print("🗑️ Đã xóa admin cũ")
    
    # Tạo admin mới với password hash
    admin = User(
        email='admin@giaohang.com',
        mat_khau='',  # Sẽ hash ở dòng dưới
        vai_tro='admin'
    )
    admin.set_password('admin123')  # ← Hash password
    
    db.session.add(admin)
    db.session.commit()
    
    print("✅ Đã tạo admin mới thành công!")
    print("   Email: admin@giaohang.com")
    print("   Password: admin123")
    print("   Password đã được hash:", admin.mat_khau[:50] + "...")