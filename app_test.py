#!/usr/bin/env python3
"""
Test Flask app without database initialization
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'phd_seminar_secret_key_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phd_seminar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Basic User model for testing
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return "Index page is working!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    return "Login page is working!"

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return "Profile page is working!"

@app.route('/dashboard')
@login_required
def dashboard():
    return "Dashboard page is working!"

if __name__ == '__main__':
    print("Starting test app without database initialization...")
    app.run(debug=True, host='0.0.0.0', port=5000)
