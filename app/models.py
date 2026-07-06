from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    image_filename = db.Column(db.String(100), nullable=True)
    video_filename = db.Column(db.String(200), nullable=True)
    live_link = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f'<Project {self.title}>'

class AboutContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    sub_description = db.Column(db.Text, nullable=True)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<AboutContent {self.headline}>'

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon_name = db.Column(db.String(50), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Service {self.title}>'

class SocialLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instagram_url = db.Column(db.String(200), nullable=True)
    facebook_url = db.Column(db.String(200), nullable=True)
    whatsapp_number = db.Column(db.String(50), nullable=True)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SocialLinks {self.id}>'
