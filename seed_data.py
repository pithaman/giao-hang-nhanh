from app import create_app, db
from app.models import User, KhachHang, TaiXe, DonHang, KhuyenMai
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    print("🌱 Đang thêm dữ liệu mẫu...")
    
    # Tạo User Admin
    admin = User(
        email='admin@giaohang.com',
        mat_khau='admin123',
        vai_tro='admin'
    )
    db.session.add(admin)
    
    # Tạo User Customer
    customer_user = User(
        email='customer@giaohang.com',
        mat_khau='customer123',
        vai_tro='khach_hang'
    )
    db.session.add(customer_user)
    db.session.flush()  # Để lấy ID
    
    # Tạo Customer
    customer = KhachHang(
        nguoi_dung_id=customer_user.id,
        ho_ten='Nguyễn Văn An',
        so_dien_thoai='0901234567',
        dia_chi='123 Kim Mã, Ba Đình, Hà Nội'
    )
    db.session.add(customer)
    db.session.flush()
    
    # Tạo User Driver
    driver_user = User(
        email='driver@giaohang.com',
        mat_khau='driver123',
        vai_tro='tai_xe'
    )
    db.session.add(driver_user)
    db.session.flush()
    
    # Tạo Driver
    driver = TaiXe(
        nguoi_dung_id=driver_user.id,
        ho_ten='Trần Văn Tài',
        so_dien_thoai='0909876543',
        bien_so_xe='29A12345',
        loai_xe='xe_may',
        trang_thai='hoat_dong',
        danh_gia=4.8,
        tong_don=0
    )
    db.session.add(driver)
    db.session.flush()
    
    # Tạo Promotion
    promotion = KhuyenMai(
        ma_khuyen_mai='GIAM10',
        loai_giam_gia='phan_tram',
        gia_tri_giam=10,
        don_toi_thieu=200000,
        giam_toi_da=50000,
        so_luong=100,
        so_luong_da_dung=0,
        ngay_het_han=datetime.utcnow() + timedelta(days=30),
        dang_hoat_dong=True
    )
    db.session.add(promotion)
    
    # Tạo Order
    ma_don = 'DH' + datetime.now().strftime('%Y%m%d%H%M%S')
    
    order = DonHang(
        khach_hang_id=customer.id,
        tai_xe_id=driver.id,
        khuyen_mai_id=None,
        ma_don=ma_don,
        dia_chi_lay='123 Kim Mã, Ba Đình, Hà Nội',
        dia_chi_giao='456 Láng Hạ, Đống Đa, Hà Nội',
        khoang_cach=5.5,
        trang_thai='cho_duyet',
        phi_van_chuyen=30000,
        tien_hang=0,
        tien_giam_gia=0,
        tong_tien=30000,
        ghi_chu='Giao hàng cẩn thận'
    )
    db.session.add(order)
    
    # Commit tất cả
    db.session.commit()
    
    print("✅ Đã thêm dữ liệu mẫu thành công!")
    print(f"   - 1 Admin user")
    print(f"   - 1 Customer")
    print(f"   - 1 Driver")
    print(f"   - 1 Promotion")
    print(f"   - 1 Order")