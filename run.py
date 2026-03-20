# run.py
from app import create_app, db
from app.models import User
import os

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Database tables created!")
    
    admin = User.query.filter_by(email='admin@giaohang.com').first()
    if not admin:
        admin = User(
            email='admin@giaohang.com',
            name='Admin',
            phone='0123456789',
            vai_tro='admin'  # ✅ STRING!
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin created: admin@giaohang.com / admin123")
    else:
        print("ℹ️ Admin already exists")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)