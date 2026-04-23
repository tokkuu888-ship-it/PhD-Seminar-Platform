#!/usr/bin/env python3
"""
Simple Flask app test without database
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World - Server is working!"

@app.route('/login')
def login():
    return "Login page is working!"

@app.route('/profile')
def profile():
    return "Profile page is working!"

if __name__ == '__main__':
    print("Starting simple test server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
