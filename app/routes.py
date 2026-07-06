from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import User, Project, AboutContent, Service, SocialLinks

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    projects = Project.query.all()
    about_content = AboutContent.query.first()
    services = Service.query.all()
    social_links = SocialLinks.query.first()
    return render_template('home.html', projects=projects, about_content=about_content, services=services, social_links=social_links)



# Admin Authentication Routes
@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('admin/login.html')


@bp.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.admin_login'))


@bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html')


# Project Management Routes
@bp.route('/admin/projects')
@login_required
def admin_projects():
    projects = Project.query.order_by(Project.date_created.desc()).all()
    return render_template('admin/manage_projects.html', projects=projects)


@bp.route('/admin/projects/new', methods=['GET', 'POST'])
@login_required
def admin_project_new():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')

        image_filename = None
        video_filename = None

        # Handle image upload
        image_file = request.files.get('image_file')
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            image_upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(image_upload_folder, exist_ok=True)
            image_file.save(os.path.join(image_upload_folder, filename))
            image_filename = filename

        # Handle video upload
        video_file = request.files.get('video_file')
        if video_file and video_file.filename:
            filename = secure_filename(video_file.filename)
            video_upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'videos')
            os.makedirs(video_upload_folder, exist_ok=True)
            video_file.save(os.path.join(video_upload_folder, filename))
            video_filename = filename

        project = Project(
            title=title,
            description=description,
            category=category,
            image_filename=image_filename,
            video_filename=video_filename
        )

        db.session.add(project)
        db.session.commit()

        flash('Project created successfully!', 'success')
        return redirect(url_for('main.admin_projects'))

    return render_template('admin/project_form.html', project=None)


@bp.route('/admin/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_project_edit(id):
    project = Project.query.get_or_404(id)

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.category = request.form.get('category')

        # Handle image upload
        image_file = request.files.get('image_file')
        if image_file and image_file.filename:
            if project.image_filename:
                old_image_path = os.path.join(current_app.root_path, 'static', 'uploads', project.image_filename)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            filename = secure_filename(image_file.filename)
            image_upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(image_upload_folder, exist_ok=True)
            image_file.save(os.path.join(image_upload_folder, filename))
            project.image_filename = filename

        # Handle video upload
        video_file = request.files.get('video_file')
        if video_file and video_file.filename:
            if project.video_filename:
                old_video_path = os.path.join(current_app.root_path, 'static', 'uploads', 'videos', project.video_filename)
                if os.path.exists(old_video_path):
                    os.remove(old_video_path)

            filename = secure_filename(video_file.filename)
            video_upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'videos')
            os.makedirs(video_upload_folder, exist_ok=True)
            video_file.save(os.path.join(video_upload_folder, filename))
            project.video_filename = filename

        db.session.commit()

        flash('Project updated successfully!', 'success')
        return redirect(url_for('main.admin_projects'))

    return render_template('admin/project_form.html', project=project)


@bp.route('/admin/projects/delete/<int:id>', methods=['POST'])
@login_required
def admin_project_delete(id):
    project = Project.query.get_or_404(id)

    if project.image_filename:
        image_path = os.path.join(current_app.root_path, 'static', 'uploads', project.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)

    if project.video_filename:
        video_path = os.path.join(current_app.root_path, 'static', 'uploads', 'videos', project.video_filename)
        if os.path.exists(video_path):
            os.remove(video_path)

    db.session.delete(project)
    db.session.commit()

    flash('Project deleted successfully!', 'success')
    return redirect(url_for('main.admin_projects'))


# About Content Management Routes
@bp.route('/admin/about', methods=['GET', 'POST'])
@login_required
def admin_about():
    about_content = AboutContent.query.first()
    
    if request.method == 'POST':
        if about_content:
            about_content.headline = request.form.get('headline')
            about_content.description = request.form.get('description')
            about_content.sub_description = request.form.get('sub_description')
        else:
            about_content = AboutContent(
                headline=request.form.get('headline'),
                description=request.form.get('description'),
                sub_description=request.form.get('sub_description')
            )
            db.session.add(about_content)
        
        db.session.commit()
        flash('About content updated successfully!', 'success')
        return redirect(url_for('main.admin_about'))
    
    return render_template('admin/about_form.html', about_content=about_content)


# Services Management Routes
@bp.route('/admin/services')
@login_required
def admin_services():
    services = Service.query.order_by(Service.date_created.desc()).all()
    return render_template('admin/manage_services.html', services=services)


@bp.route('/admin/services/new', methods=['GET', 'POST'])
@login_required
def admin_service_new():
    if request.method == 'POST':
        service = Service(
            title=request.form.get('title'),
            description=request.form.get('description'),
            icon_name=request.form.get('icon_name')
        )
        db.session.add(service)
        db.session.commit()
        flash('Service created successfully!', 'success')
        return redirect(url_for('main.admin_services'))
    
    return render_template('admin/service_form.html', service=None)


@bp.route('/admin/services/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_service_edit(id):
    service = Service.query.get_or_404(id)
    
    if request.method == 'POST':
        service.title = request.form.get('title')
        service.description = request.form.get('description')
        service.icon_name = request.form.get('icon_name')
        db.session.commit()
        flash('Service updated successfully!', 'success')
        return redirect(url_for('main.admin_services'))
    
    return render_template('admin/service_form.html', service=service)


@bp.route('/admin/services/delete/<int:id>', methods=['POST'])
@login_required
def admin_service_delete(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('main.admin_services'))


# Social Links Management Routes
@bp.route('/admin/social-links', methods=['GET', 'POST'])
@login_required
def admin_social_links():
    social_links = SocialLinks.query.first()
    
    if request.method == 'POST':
        if social_links:
            social_links.instagram_url = request.form.get('instagram_url')
            social_links.facebook_url = request.form.get('facebook_url')
            social_links.whatsapp_number = request.form.get('whatsapp_number')
        else:
            social_links = SocialLinks(
                instagram_url=request.form.get('instagram_url'),
                facebook_url=request.form.get('facebook_url'),
                whatsapp_number=request.form.get('whatsapp_number')
            )
            db.session.add(social_links)
        
        db.session.commit()
        flash('Social links updated successfully!', 'success')
        return redirect(url_for('main.admin_social_links'))
    
    return render_template('admin/social_links_form.html', social_links=social_links)