#!/usr/bin/env python3
"""
PhD Seminar Platform Deployment Script
"""

import os
import time
from flask import Flask
from app import app
import pyngrok

def deploy_platform():
    """Deploy the PhD Seminar Platform with ngrok tunnel"""
    
    print("🚀 Starting PhD Seminar Platform Deployment...")
    print("=" * 60)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    ngrok_authtoken = os.getenv('NGROK_AUTHTOKEN')
    
    if not ngrok_authtoken or ngrok_authtoken == 'YOUR_NGROK_AUTHTOKEN_HERE':
        print("❌ Ngrok authtoken not configured!")
        print("Please update your .env file with your ngrok authtoken:")
        print("1. Go to https://dashboard.ngrok.com/auth")
        print("2. Copy your authtoken")
        print("3. Update .env file: NGROK_AUTHTOKEN=your_token_here")
        return
    
    # Configure ngrok
    try:
        from pyngrok import ngrok
        ngrok.set_auth_token(ngrok_authtoken)
        print("✅ Ngrok authentication successful")
    except Exception as e:
        print(f"❌ Ngrok authentication failed: {e}")
        return
    
    # Start ngrok tunnel
    try:
        print("🌐 Starting ngrok tunnel...")
        ngrok_tunnel = ngrok.connect(5000, bind_tls=True)
        public_url = ngrok_tunnel.public_url
        
        print("\n" + "=" * 60)
        print("🎉 DEPLOYMENT SUCCESSFUL!")
        print("=" * 60)
        print(f"🌍 Public URL: {public_url}")
        print(f"📱 Mobile Access: {public_url}")
        print(f"🏠 Local Access: http://localhost:5000")
        print("=" * 60)
        
        print("\n📋 Demo Accounts:")
        print("┌─────────────┬──────────────┬─────────────┐")
        print("│    Role     │   Username   │   Password  │")
        print("├─────────────┼──────────────┼─────────────┤")
        print("│    Dean     │ dr_yenesew_  │  admin123   │")
        print("│             │ mengiste     │             │")
        print("│  Professor  │  professor1  │   prof123   │")
        print("│ PhD Candidate│   student1   │ student123  │")
        print("└─────────────┴──────────────┴─────────────┘")
        
        print(f"\n🎓 Dean Name: Dr. Yenesew Mengiste")
        print(f"👨‍🏫 Professor: Professor Dereje Hailu")
        print(f"👩‍🎓 Student: Tokuma Adamu")
        
        print("\n📱 Platform Features:")
        print("✅ User Registration (Students & Professors)")
        print("✅ Profile Editing")
        print("✅ Seminar Scheduling")
        print("✅ Progress Reports")
        print("✅ Feedback System")
        print("✅ Mobile & Desktop Compatible")
        
        print(f"\n🔗 Share this URL: {public_url}")
        print("📧 Anyone with the link can access the platform!")
        
        # Start Flask app
        print(f"\n🚀 Starting web server...")
        print("📝 Press Ctrl+C to stop the deployment")
        print("=" * 60)
        
        app.run(host='0.0.0.0', port=5000, debug=False)
        
    except Exception as e:
        print(f"❌ Failed to start ngrok tunnel: {e}")
        print("🏠 Running locally only at: http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    deploy_platform()
