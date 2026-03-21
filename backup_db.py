# backup_db.py
import os
import pymysql
from datetime import datetime

# Connect to MySQL
conn = pymysql.connect(
    host='localhost',
    user='giao_hang_user',
    password='GiaoHang2026!',
    database='giao_hang_nhanh'
)

# Export data
with conn.cursor() as cursor:
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    
    cursor.execute("SELECT * FROM don_hang")
    orders = cursor.fetchall()

# Save to file
backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(backup_file, 'w', encoding='utf-8') as f:
    f.write(f"=== BACKUP {datetime.now()} ===\n\n")
    f.write(f"Users: {len(users)}\n")
    f.write(f"Orders: {len(orders)}\n")

print(f"✅ Backup saved to {backup_file}")
conn.close()