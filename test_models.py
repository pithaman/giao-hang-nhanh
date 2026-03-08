from app import create_app, db
from app.models import User, KhachHang, TaiXe, DonHang, KhuyenMai

app = create_app()

with app.app_context():
    print("=" * 50)
    print("🔍 KIỂM TRA MODELS")
    print("=" * 50)
    
    # Test User
    print("\n📊 Users:")
    users = User.query.all()
    print(f"   Tổng số users: {len(users)}")
    for user in users[:5]:  # Hiển thị 5 users đầu
        print(f"   - {user.email} ({user.vai_tro})")
    
    # Test Customer
    print("\n👥 Customers:")
    customers = KhachHang.query.all()
    print(f"   Tổng số customers: {len(customers)}")
    for kh in customers[:5]:
        print(f"   - {kh.ho_ten} ({kh.so_dien_thoai})")
    
    # Test Driver
    print("\n🚚 Drivers:")
    drivers = TaiXe.query.all()
    print(f"   Tổng số drivers: {len(drivers)}")
    for tx in drivers[:5]:
        print(f"   - {tx.ho_ten} ({tx.bien_so_xe}) - {tx.trang_thai}")
    
    # Test Orders
    print("\n📦 Orders:")
    orders = DonHang.query.all()
    print(f"   Tổng số orders: {len(orders)}")
    for dh in orders[:5]:
        print(f"   - {dh.ma_don}: {dh.tong_tien}đ - {dh.get_trang_thai_display()}")
    
    # Test Promotions
    print("\n🎁 Promotions:")
    promotions = KhuyenMai.query.all()
    print(f"   Tổng số promotions: {len(promotions)}")
    for km in promotions:
        print(f"   - {km.ma_khuyen_mai}: {km.gia_tri_giam} ({km.loai_giam_gia})")
    
    print("\n" + "=" * 50)
    print("✅ KIỂM TRA HOÀN TẤT!")
    print("=" * 50)