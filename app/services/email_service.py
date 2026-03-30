# app/services/email_service.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from threading import Thread
from flask import current_app

def send_async_email(api_key, from_email, from_name, to_email, subject, html_content):
    """Gửi email bất đồng bộ qua SendGrid"""
    try:
        message = Mail(
            from_email=(from_email, from_name),
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        
        print(f"✅ Email sent! Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def send_email(subject, to_email, html_content):
    """Gửi email qua SendGrid - FIX VERSION"""
    
    import os
    
    # ✅ Đọc TRỰC TIẾP từ os.environ (đã được load_dotenv() set)
    api_key = os.environ.get('SENDGRID_API_KEY')
    from_email = os.environ.get('SENDGRID_FROM_EMAIL')
    from_name = os.environ.get('SENDGRID_FROM_NAME', 'Giao Hàng Nhanh')
    
    # Debug prints (xóa sau khi fix xong)
    print(f"🔍 [FIX] API Key: {'✅ SET' if api_key else '❌ NONE'}")
    print(f"🔍 [FIX] From Email: {from_email}")
    
    if not api_key or not from_email:
        print("⚠️ SendGrid not configured!")
        return None
    
    # ... rest of code giữ nguyên
    try:
        message = Mail(
            from_email=(from_email, from_name),
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        
        print(f"✅ Email sent! Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def send_order_confirmation_email(don_hang):
    """Gửi email xác nhận đơn hàng"""
    
    subject = f'✅ Xác nhận đơn hàng {don_hang.ma_don}'
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 20px auto; background: white; border-radius: 10px; overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #007bff, #0056b3); color: white; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; }}
            .order-info {{ background: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 8px; }}
            .price {{ font-size: 24px; color: #28a745; font-weight: bold; }}
            .button {{ display: inline-block; padding: 12px 30px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📦 Giao Hàng Nhanh</h1>
                <p>Xác nhận đơn hàng thành công</p>
            </div>
            <div class="content">
                <p>Xin chào <strong>{don_hang.customer.name}</strong>,</p>
                <p>Cảm ơn bạn đã đặt hàng!</p>
                
                <div class="order-info">
                    <h3>📋 Chi tiết đơn hàng</h3>
                    <p><strong>Mã đơn:</strong> {don_hang.ma_don}</p>
                    <p><strong>🏠 Lấy tại:</strong> {don_hang.dia_chi_lay}</p>
                    <p><strong>🎯 Giao đến:</strong> {don_hang.dia_chi_giao}</p>
                    <p><strong>💰 Tổng tiền:</strong> <span class="price">{don_hang.tong_tien:,.0f}đ</span></p>
                    <p><strong>📍 Trạng thái:</strong> ⏳ {don_hang.trang_thai}</p>
                </div>
                
                <p style="text-align: center;">
                    <a href="https://giao-hang-nhanh.onrender.com/customer/track/{don_hang.ma_don}" class="button">
                        🔍 Theo dõi đơn hàng
                    </a>
                </p>
            </div>
            <div class="footer">
                <p>© 2026 Giao Hàng Nhanh</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    send_email(subject, don_hang.customer.email, html_content)
    print(f"📧 Email sent to {don_hang.customer.email}")