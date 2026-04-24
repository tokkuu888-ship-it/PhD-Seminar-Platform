from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'phd_seminar_secret_key_2026'
database_url = os.environ.get('DATABASE_URL')

if database_url:
    # 1. Standardize the prefix for pg8000
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql+pg8000://', 1)
    elif database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql+pg8000://', 1)
    
    # 2. Clean EVERYTHING after the database name
    # This removes ?sslmode=require, &channel_binding=require, etc.
    if '?' in database_url:
        database_url = database_url.split('?')[0]

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Explicitly enable SSL the way pg8000 likes it
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {"ssl_context": True}
}

db = SQLAlchemy(app)

with app.app_context():
    try:
        # This creates the tables in your new Neon phd_seminar_db
        db.create_all()
        print("🚀 NEON DATABASE INITIALIZED: Tables Created!")
    except Exception as e:
        print(f"❌ Initialization Error: {e}")

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'dean', 'professor', 'phd_candidate'
    full_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Seminar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=90)
    phase = db.Column(db.String(50), default='presentation')  # presentation, peer_review, faculty_viva, mentorship
    presenter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, in_progress, completed, cancelled
    meeting_link = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    presenter = db.relationship('User', backref='presented_seminars')

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='availabilities')

class ProgressReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seminar_id = db.Column(db.Integer, db.ForeignKey('seminar.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    chapter_focus = db.Column(db.String(200))
    achievements = db.Column(db.Text)
    challenges = db.Column(db.Text)
    next_steps = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('User', backref='progress_reports')
    seminar = db.relationship('Seminar', backref='progress_reports')

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seminar_id = db.Column(db.Integer, db.ForeignKey('seminar.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback_type = db.Column(db.String(20), nullable=False)  # peer, faculty
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # 1-5 scale
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    seminar = db.relationship('Seminar', backref='feedbacks')
    reviewer = db.relationship('User', backref='given_feedbacks')

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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        department = request.form.get('department')
        role = request.form.get('role')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('register'))
        
        # Create new user
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

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.email = request.form.get('email')
        current_user.department = request.form.get('department')
        
        # Check if password change is requested
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

@app.route('/dashboard')
@login_required
def dashboard():
    upcoming_seminars = Seminar.query.filter(
        Seminar.scheduled_date > datetime.utcnow(),
        Seminar.status == 'scheduled'
    ).order_by(Seminar.scheduled_date).all()
    
    my_seminars = Seminar.query.filter_by(presenter_id=current_user.id).all()
    my_reports = ProgressReport.query.filter_by(student_id=current_user.id).all()
    
    return render_template('dashboard.html', 
                         upcoming_seminars=upcoming_seminars,
                         my_seminars=my_seminars,
                         my_reports=my_reports)

@app.route('/seminars')
@login_required
def seminars():
    seminars = Seminar.query.order_by(Seminar.scheduled_date.desc()).all()
    return render_template('seminars.html', seminars=seminars)

@app.route('/seminar/<int:seminar_id>')
@login_required
def seminar_detail(seminar_id):
    seminar = Seminar.query.get_or_404(seminar_id)
    progress_report = ProgressReport.query.filter_by(seminar_id=seminar_id).first()
    feedbacks = Feedback.query.filter_by(seminar_id=seminar_id).all()
    
    return render_template('seminar_detail.html', 
                         seminar=seminar,
                         progress_report=progress_report,
                         feedbacks=feedbacks)

@app.route('/schedule_seminar', methods=['GET', 'POST'])
@login_required
def schedule_seminar():
    if current_user.role not in ['dean', 'professor']:
        flash('Only faculty can schedule seminars', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        scheduled_date = datetime.strptime(request.form.get('scheduled_date'), '%Y-%m-%d %H:%M')
        presenter_id = request.form.get('presenter_id')
        
        seminar = Seminar(
            title=title,
            description=description,
            scheduled_date=scheduled_date,
            presenter_id=presenter_id
        )
        
        db.session.add(seminar)
        db.session.commit()
        
        flash('Seminar scheduled successfully!', 'success')
        return redirect(url_for('seminars'))
    
    phd_candidates = User.query.filter_by(role='phd_candidate').all()
    return render_template('schedule_seminar.html', phd_candidates=phd_candidates)

@app.route('/availability', methods=['GET', 'POST'])
@login_required
def availability():
    if request.method == 'POST':
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        start_time = datetime.strptime(request.form.get('start_time'), '%H:%M').time()
        end_time = datetime.strptime(request.form.get('end_time'), '%H:%M').time()
        
        availability = Availability(
            user_id=current_user.id,
            date=date,
            start_time=start_time,
            end_time=end_time
        )
        
        db.session.add(availability)
        db.session.commit()
        
        flash('Availability updated successfully!', 'success')
        return redirect(url_for('availability'))
    
    availabilities = Availability.query.filter_by(user_id=current_user.id).order_by(Availability.date).all()
    return render_template('availability.html', availabilities=availabilities)

@app.route('/submit_report/<int:seminar_id>', methods=['GET', 'POST'])
@login_required
def submit_report(seminar_id):
    seminar = Seminar.query.get_or_404(seminar_id)
    
    if seminar.presenter_id != current_user.id:
        flash('You can only submit reports for your own seminars', 'error')
        return redirect(url_for('dashboard'))
    
    existing_report = ProgressReport.query.filter_by(seminar_id=seminar_id).first()
    if existing_report:
        flash('You have already submitted a report for this seminar', 'error')
        return redirect(url_for('seminar_detail', seminar_id=seminar_id))
    
    if request.method == 'POST':
        content = request.form.get('content')
        chapter_focus = request.form.get('chapter_focus')
        achievements = request.form.get('achievements')
        challenges = request.form.get('challenges')
        next_steps = request.form.get('next_steps')
        
        report = ProgressReport(
            student_id=current_user.id,
            seminar_id=seminar_id,
            content=content,
            chapter_focus=chapter_focus,
            achievements=achievements,
            challenges=challenges,
            next_steps=next_steps
        )
        
        db.session.add(report)
        db.session.commit()
        
        flash('Progress report submitted successfully!', 'success')
        return redirect(url_for('seminar_detail', seminar_id=seminar_id))
    
    return render_template('submit_report.html', seminar=seminar)

@app.route('/submit_feedback/<int:seminar_id>', methods=['GET', 'POST'])
@login_required
def submit_feedback(seminar_id):
    seminar = Seminar.query.get_or_404(seminar_id)
    
    if current_user.role == 'phd_candidate':
        feedback_type = 'peer'
    else:
        feedback_type = 'faculty'
    
    existing_feedback = Feedback.query.filter_by(
        seminar_id=seminar_id,
        reviewer_id=current_user.id
    ).first()
    
    if existing_feedback:
        flash('You have already submitted feedback for this seminar', 'error')
        return redirect(url_for('seminar_detail', seminar_id=seminar_id))
    
    if request.method == 'POST':
        content = request.form.get('content')
        rating = request.form.get('rating')
        
        feedback = Feedback(
            seminar_id=seminar_id,
            reviewer_id=current_user.id,
            feedback_type=feedback_type,
            content=content,
            rating=rating
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('seminar_detail', seminar_id=seminar_id))
    
    return render_template('submit_feedback.html', seminar=seminar, feedback_type=feedback_type)

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

if __name__ == '__main__':
    try:
        with app.app_context():
            create_default_users()
    except Exception as e:
        print(f"Database initialization error: {e}")
        print("Starting server without database initialization...")
    
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', '1') == '1'

    print(" * Starting PhD Seminar Platform...")
    print(f" * Local access: http://localhost:{port}")
    print(" * Mobile access: http://10.5.19.50:5000 (same network)")
    print(" * Press Ctrl+C to stop the server")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
