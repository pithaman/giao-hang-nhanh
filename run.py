from app import create_app, db
from app.models import User
import os

app = create_app()

# ✅ AUTO-INIT DATABASE KHI APP CHẠY
with app.app_context():
    try:
        # Tạo tất cả tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Tạo admin account
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
            print("✅ Admin created: admin@giaohang.com / admin123")
        else:
            print("ℹ️ Admin already exists")
            
        print("✅ Database initialization complete!")
        
    except Exception as e:
        print(f"⚠️ Database init warning: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)