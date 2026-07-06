from app import app, db
from app.models import AboutContent, Service

with app.app_context():
    # Create new tables only if they don't exist
    db.create_all()
    print('Database migration completed successfully!')
    print('New tables (AboutContent, Service) have been added without affecting existing data.')
