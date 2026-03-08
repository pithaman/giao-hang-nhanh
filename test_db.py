from app import create_app, db
from app.models import User, KhachHang, TaiXe, DonHang

app = create_app()

with app.app_context():
    try:
        # Test connection
        users_count = User.query.count()
        customers_count = KhachHang.query.count()
        drivers_count = TaiXe.query.count()
        orders_count = DonHang.query.count()
        
        print("✅ KẾT NỐI DATABASE THÀNH CÔNG!")
        print(f"📊 Thống kê:")
        print(f"   - Users: {users_count}")
        print(f"   - Customers: {customers_count}")
        print(f"   - Drivers: {drivers_count}")
        print(f"   - Orders: {orders_count}")
        
    except Exception as e:
        print(f"❌ LỖI: {e}")