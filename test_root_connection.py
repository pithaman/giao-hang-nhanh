# test_root_connection.py
from dotenv import load_dotenv
import os
import pymysql

load_dotenv()

print("🔍 Testing MySQL connection with root...")
print("-" * 40)

try:
    conn = pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user='root',
        password=os.getenv('MYSQL_PASSWORD', 'root'),  # Thử 'root' hoặc ''
        database=os.getenv('MYSQL_DB', 'giao_hang_nhanh')
    )
    print("✅ Connected to MySQL as root!")
    
    # Create database if not exists
    with conn.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS giao_hang_nhanh CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ Database 'giao_hang_nhanh' ready!")
    
    conn.close()
    print("✅ Test successful!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\n💡 Try these passwords:")
    print("   - Empty password: ''")
    print("   - Default XAMPP: ''")
    print("   - Default WAMP: 'root'")