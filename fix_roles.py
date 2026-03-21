# fix_roles.py
"""
Script fix vai_tro trong database - chuyển về lowercase
"""
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    print("🔄 Fixing user roles to lowercase...")
    
    users = User.query.all()
    for user in users:
        old_role = user.vai_tro
        # Convert to lowercase
        user.vai_tro = (user.vai_tro or 'customer').lower().strip()
        
        if old_role != user.vai_tro:
            print(f"   {user.email}: '{old_role}' → '{user.vai_tro}'")
    
    db.session.commit()
    print("✅ Done! All roles converted to lowercase.")
    
    # Verify
    print("\n📋 Verification:")
    for user in User.query.all():
        print(f"   {user.email}: vai_tro = '{user.vai_tro}'")