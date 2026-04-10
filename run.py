# run.py
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # ✅ Render yêu cầu bind đến port từ environment variable
    port = int(os.environ.get('PORT', 10000))
    
    # Debug log
    print(f"🚀 Starting app on port {port}")
    
    app.run(
        host='0.0.0.0',  # Bind tất cả interfaces
        port=port,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )