from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Check if admin user already exists
    existing_admin = User.query.filter_by(username='admin').first()
    
    if existing_admin:
        print('Admin user already exists!')
        print(f'Username: {existing_admin.username}')
    else:
        # Create admin user
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123')
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print('Admin user created successfully!')
        print('Username: admin')
        print('Password: admin123')
        print('\nPlease change the password after first login!')
