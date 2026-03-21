# test_env.py
from dotenv import load_dotenv
import os

print("🔍 Testing .env file...")
print("-" * 40)

load_dotenv()

print('✅ .env loaded successfully!')
print(f'📊 MYSQL_USER: {os.getenv("MYSQL_USER")}')
print(f'📊 MYSQL_HOST: {os.getenv("MYSQL_HOST")}')
print(f'📊 MYSQL_PORT: {os.getenv("MYSQL_PORT")}')
print(f'📊 MYSQL_DB: {os.getenv("MYSQL_DB")}')
print(f'📊 SECRET_KEY: {os.getenv("SECRET_KEY")}')
print("-" * 40)
print('✅ All environment variables loaded!')