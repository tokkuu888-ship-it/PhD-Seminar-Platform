#!/usr/bin/env python3
"""
PhD Seminar Platform - Render Production Version
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configuration for Render
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'phd_seminar_secret_key_2026')
database_url = os.environ.get('DATABASE_URL', 'sqlite:///phd_seminar.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql+pg8000://', 1)
elif database_url.startswith('postgresql://'):
    database_url = database_url.replace('postgresql://', 'postgresql+pg8000://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Seminar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    presenter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.Time, nullable=False)
    meeting_link = db.Column(db.String(500))
    status = db.Column(db.String(20), default='scheduled')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    presenter = db.relationship('User', backref='seminars')

class ProgressReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seminar_id = db.Column(db.Integer, db.ForeignKey('seminar.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chapter_focus = db.Column(db.String(200), nullable=False)
    achievements = db.Column(db.Text, nullable=False)
    challenges = db.Column(db.Text, nullable=False)
    next_steps = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    seminar = db.relationship('Seminar', backref='progress_reports')
    student = db.relationship('User', backref='submitted_reports')

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seminar_id = db.Column(db.Integer, db.ForeignKey('seminar.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback_type = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    seminar = db.relationship('Seminar', backref='feedback')
    reviewer = db.relationship('User', backref='given_feedback')

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='available')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='availability')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        role = request.form.get('role')
        department = request.form.get('department')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
            full_name=full_name,
            department=department
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.email = request.form.get('email')
        current_user.department = request.form.get('department')
        
        new_password = request.form.get('new_password')
        if new_password:
            current_password = request.form.get('current_password')
            if check_password_hash(current_user.password_hash, current_password):
                current_user.password_hash = generate_password_hash(new_password)
                flash('Password updated successfully', 'success')
            else:
                flash('Current password is incorrect', 'error')
                return redirect(url_for('profile'))
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html')

@app.route('/seminars')
@login_required
def seminars():
    seminars = Seminar.query.order_by(Seminar.date.desc()).all()
    return render_template('seminars.html', seminars=seminars)

@app.route('/seminar/<int:seminar_id>')
@login_required
def seminar_detail(seminar_id):
    seminar = Seminar.query.get_or_404(seminar_id)
    return render_template('seminar_detail.html', seminar=seminar)

@app.route('/schedule_seminar', methods=['GET', 'POST'])
@login_required
def schedule_seminar():
    if current_user.role not in ['dean', 'professor']:
        flash('Only deans and professors can schedule seminars', 'error')
        return redirect(url_for('seminars'))
    
    if request.method == 'POST':
        seminar = Seminar(
            title=request.form.get('title'),
            description=request.form.get('description'),
            presenter_id=current_user.id,
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d'),
            time=datetime.strptime(request.form.get('time'), '%H:%M').time(),
            meeting_link=request.form.get('meeting_link')
        )
        
        db.session.add(seminar)
        db.session.commit()
        
        flash('Seminar scheduled successfully!', 'success')
        return redirect(url_for('seminars'))
    
    return render_template('schedule_seminar.html')

@app.route('/availability')
@login_required
def availability():
    return render_template('availability.html')

def create_default_users():
    """Create default users for demonstration"""
    if not User.query.filter_by(username='dr_yenesew_mengiste').first():
        dean = User(
            username='dr_yenesew_mengiste',
            email='dean@university.edu',
            password_hash=generate_password_hash('admin123'),
            role='dean',
            full_name='Dr. Yenesew Mengiste',
            department='Computer Science'
        )
        db.session.add(dean)
    
    if not User.query.filter_by(username='professor1').first():
        professor = User(
            username='professor1',
            email='prof1@university.edu',
            password_hash=generate_password_hash('prof123'),
            role='professor',
            full_name='Professor Dereje Hailu',
            department='Computer Science'
        )
        db.session.add(professor)
    
    if not User.query.filter_by(username='student1').first():
        student = User(
            username='student1',
            email='student1@university.edu',
            password_hash=generate_password_hash('student123'),
            role='phd_candidate',
            full_name='Tokuma Adamu',
            department='Computer Science'
        )
        db.session.add(student)
    
    db.session.commit()

# Initialize database on first run
with app.app_context():
    db.create_all()
    create_default_users()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
