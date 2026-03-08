import pymysql

try:
    # Password: 05092005
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='05092005',
        database='giao_hang_don_le'
    )
    print("✅ KẾT NỐI MYSQL THÀNH CÔNG!")
    
    # Test query
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()
        print(f"📦 Database hiện tại: {result[0]}")
        
        # Đếm số bảng
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print(f"📊 Số bảng trong database: {len(tables)}")
        
        # Hiển thị các bảng
        print("\n📋 Danh sách bảng:")
        for table in tables:
            print(f"   - {table[0]}")
    
    connection.close()
    
except pymysql.err.OperationalError as e:
    print(f"❌ LỖI KẾT NỐI: {e}")
except Exception as e:
    print(f"❌ LỖI KHÁC: {e}")