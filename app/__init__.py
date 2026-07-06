from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'fejhdhdcx9954'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website_webify.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.admin_login'
    
    # Import models BEFORE create_all, so SQLAlchemy knows about them
    from app.models import User, Project, AboutContent, Service, SocialLinks
    
    # Create database tables
    with app.app_context():
        db.create_all()
        import os
        print(">>> DB PATH:", os.path.abspath(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')))
        from sqlalchemy import inspect
        print(">>> TABLES:", inspect(db.engine).get_table_names())
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes import bp
    app.register_blueprint(bp)
    
    return app